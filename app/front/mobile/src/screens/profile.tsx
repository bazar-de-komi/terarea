import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, Image, Alert, TouchableOpacity } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../components/CustomersInput/CustomerInput";
import BackButton from "../components/BackButton/backButton";
import SocialAuthButton from "../components/SocialAuthButton";

import Header from "../components/Header/header";

// import ProfileLogo from "../../assets/profilLogo.png";
import { getValue } from "../components/StoreData/storeData";
import { queries } from "../../back-endConnection/querier";

const Profile = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const navigation = useNavigation();

    const handleBackButton = () => {
        navigation.goBack();
    }

    const handleSaveChangeButton = async () => {
        try {
            const token = await getValue("token");
            let body = {};
            if (username !== "") {
                body["username"] = username;
            }
            if (email !== "") {
                const emailRegex: RegExp = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;

                function isValidEmail(email: string): boolean {
                    return emailRegex.test(email);
                }

                if (isValidEmail(email) === false) {
                    Alert.alert("The email you entered is not a valid email.")
                    return;
                }
                body["email"] = email;
            }
            if (password !== "") {
                body["password"] = password;
            }
            await queries.patch("/api/v1/user", { body }, token);
            Alert.alert("Your information was updated successfully.");
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to change your information.");
        }
    }

    useEffect(() => {
        const getUserInfo = async () => {
            try {
                const token = await getValue("token");
                const response = await queries.get("/api/v1/user", {}, token);
                setUsername(response.msg.username);
                setEmail(response.msg.email);
            } catch (error) {
                console.error(error);
                Alert.alert("Failed to retrieve your information.");
            }
        };
        getUserInfo();
    }, []);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            {/* <Text style={styles.homeTitle}>Account Setting</Text> */}
            <View style={styles.backButtonContainer}>
                <BackButton
                    text={" < "}
                    onPress={handleBackButton}
                />
            </View>
            {/* <Text style={styles.homeProfileTxt}>Profile</Text> */}
            {/* <Image
                source={ProfileLogo}
                style={styles.profileLogo}
            /> */}
            {/* <Text style={styles.personalizeTxt}>Personalize your account by linking a profil from another service.</Text> */}
            <Text style={styles.homeAccountTitle}>Account</Text>
            <View style={{ paddingTop: 30 }}>
                <Text style={styles.optionTitle}>Username</Text>
                <View style={styles.homeNavigation}>
                </View>
                <View style={styles.searchBar}>
                    <CustomerInput
                        value={username}
                        setValue={setUsername}
                        placeholder="Your username"
                    />
                </View>
                <Text style={styles.optionTitle}>Password</Text>
                <View style={styles.searchBar}>
                    <CustomerInput
                        value={password}
                        setValue={setPassword}
                        placeholder="Can't be retrieved due to security"
                        secureTextEntry={true}
                    />
                </View>
                <Text style={styles.optionTitle}>Email</Text>
                <View style={styles.searchBar}>
                    <CustomerInput
                        value={email}
                        setValue={setEmail}
                        placeholder="Your email"
                    />
                </View>
                {/* <TouchableOpacity onPress={handleSaveChangeButton}>
                    <Text>Touche here please</Text>
                </TouchableOpacity> */}
            </View>
            {/* <Text style={styles.homeTitle}>Linked accounts</Text> */}
            {/* <SocialAuthButton /> */}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 10,
        marginLeft: 90,
        alignItems: 'center',
    },
    backButtonContainer: {
        left: 160,
        marginTop: 90,
        marginBottom: -118
    },
    homeAccountTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 10,
        marginLeft: 140,
        alignItems: 'center',
    },
    homeProfileTxt: {
        fontSize: 24,
        fontWeight: 'bold',
        marginLeft: 50,
    },
    personalizeTxt: {
        fontSize: 18,
        marginLeft: 150,
        bottom: 50,
    },
    optionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginLeft: 50,
        paddingTop: 10
    },
    profileLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: 60,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
    },
    searchBar: {
        marginBottom: 10,
        width: '100%',
        left: 50,
    },
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
});

export default Profile;
