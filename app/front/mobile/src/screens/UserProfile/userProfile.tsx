import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, Alert, TouchableOpacity } from 'react-native'

import CustomInput from "../../components/CustomInput/customInput";
import Header from "../../components/Header/header";
import { getValue } from "../../components/StoreData/storeData";
import { queries } from "../../../back-endConnection/querier";
import CustomButton from "../../components/CustomButton/customButton";

const Profile = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");

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
            const response = await queries.patch("/api/v1/user", { body }, token);
            if (response.resp === "success") {
                Alert.alert("Your information was updated successfully.");
            }
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
                if (response.resp === "success") {
                    setUsername(response.msg.username);
                    setEmail(response.msg.email);
                }
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
            <Text style={styles.homeAccountTitle}>Account</Text>
            <View style={{ paddingTop: 30 }}>
                <Text style={styles.optionTitle}>Username</Text>
                <View style={styles.input}>
                    <CustomInput
                        value={username}
                        setValue={setUsername}
                        placeholder="Your username"
                        secureTextEntry={false}
                    />
                </View>
                <Text style={styles.optionTitle}>Password</Text>
                <View style={styles.input}>
                    <CustomInput
                        value={password}
                        setValue={setPassword}
                        placeholder="Can't be retrieved due to security"
                        secureTextEntry={true}
                    />
                </View>
                <Text style={styles.optionTitle}>Email</Text>
                <View style={styles.input}>
                    <CustomInput
                        value={email}
                        setValue={setEmail}
                        placeholder="Your email"
                        secureTextEntry={false}
                    />
                </View>
                <View style={styles.saveButtonContainer}>
                    <CustomButton
                        text="Save changes"
                        type="PRIMARY"
                        bgColor="blue"
                        fgColor="white"
                        icon={null}
                        onPress={handleSaveChangeButton}
                    />
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeAccountTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        marginTop: 20,
        marginBottom: 10,
        textAlign: 'center'
    },
    optionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginLeft: 50,
        paddingTop: 10
    },
    input: {
        marginBottom: 10,
        width: '100%',
        left: 50
    },
    saveButtonContainer: {
        alignItems: 'center'
    }
});

export default Profile;
