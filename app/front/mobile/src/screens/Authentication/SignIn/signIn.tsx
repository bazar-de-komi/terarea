import React, { useState } from "react";
import { View, Text, Image, StyleSheet, useWindowDimensions, ScrollView, Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { queries } from "../../../../back-endConnection/querier";
import { storeValue } from "../../../components/StoreData/storeData";

import CustomerInput from "../../../components/CustomersInput";
import CustomerButton from '../../../components/CustomerButton';
import SocialLogo from '../../../components/SocialAuthButton/socialAuthButton';
import Or from '../../../components/SocialAuthButton/OrLine';

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

const SignIn = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { height } = useWindowDimensions();
    const navigation = useNavigation();

    const handleSignInButton = async () => {
        if (email === '') {
            Alert.alert("You must enter an email.");
            return;
        }
        if (password === '') {
            Alert.alert("You must enter a password.");
            return;
        }
        const emailRegex: RegExp = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;

        function isValidEmail(email: string): boolean {
            return emailRegex.test(email);
        }

        if (isValidEmail(email) === false) {
            Alert.alert("The email you entered is not a valid email.")
            return;
        }
        setIsSubmitting(true);
        const account = {
            email: email,
            password: password,
        };
        try {
            const result = await queries.post("/api/v1/login", account);
            if (result.token) {
                storeValue('token', result.token);
                navigation.navigate("Applets");
            } else {
                setError("Identifiant or password incorrect");
                Alert.alert("ID or password incorrect");
            }
        } catch (error) {
            console.error("Sign error: ", error);
            setError("Error to connect. Please check your id or your password");
        } finally {
            setIsSubmitting(false);
        }
    }

    const handleForgotPasswordButton = () => {
        navigation.navigate("Forgot password");
    }

    const handleSignUpButton = () => {
        navigation.navigate("Sign Up");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backgroundContainer}>
                <Image
                    source={AreaLogo}
                    style={[styles.areaLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
                />
                <View style={styles.SignInContainer}>
                    <Text style={styles.headerText}>Sign In</Text>
                    <CustomerInput
                        placeholder="Email"
                        value={email}
                        setValue={setEmail}
                        secureTextEntry={false}
                    />
                    <CustomerInput
                        placeholder="Password"
                        value={password}
                        setValue={setPassword}
                        secureTextEntry={true}
                    />

                    <CustomerButton
                        text="Get started"
                        onPress={handleSignInButton}
                        bgColor={"#666"}
                        fgColor={"white"}
                        icon={""}
                        type={""}
                    />
                    <Or />
                    <SocialLogo />
                    <CustomerButton
                        text="Forgot your password ?"
                        onPress={handleForgotPasswordButton}
                        type="TERTIARY"
                        bgColor=""
                        fgColor="black"
                        icon=""
                    />
                    <CustomerButton
                        text="Don't have an account ? Sign up here"
                        onPress={handleSignUpButton}
                        type="TERTIARY"
                        bgColor=""
                        fgColor="black"
                        icon={""}
                    />
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    backgroundContainer: {
        marginTop: 20,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#F5F5F5',
    },
    SignInContainer: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: '#e0d8d7',
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
    },
    areaLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 100,
        marginBottom: 30,
    },
    headerText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
});

export default SignIn;
