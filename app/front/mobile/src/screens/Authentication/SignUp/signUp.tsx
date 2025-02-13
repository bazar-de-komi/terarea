import React, { useState } from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions, Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from '../../../components/CustomerButton/CustomerButton';
import SocialButton from '../../../components/SocialAuthButton/socialAuthButton';
import { storeValue } from '../../../components/StoreData/storeData';

import OrLine from "../../../components/SocialAuthButton/OrLine";
import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

import { queries } from "../../../../back-endConnection/querier";

const SignUp = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { height } = useWindowDimensions();

    const navigation = useNavigation();

    const handleSignInButton = async () => {
        if (email === '') {
            Alert.alert("You must enter an email.");
            return;
        }
        if (password === '' || repeatPassword === '') {
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
        if (password !== repeatPassword) {
            Alert.alert("Wrong password");
            return;
        }
        setIsSubmitting(true);

        const newUser = {
            email: email,
            password: password,
        };
        try {
            const response = await queries.post("/api/v1/register", newUser);
            if (response.token) {
                storeValue("token", response.token)
                Alert.alert("Sign up sucessful");
                navigation.navigate('Applets');
            } else {
                setError("Try again");
            }
        } catch (err) {
            console.error("Sign up error: ", err);
            setError("Error during sign up, try again");
        } finally {
            setIsSubmitting(false);
        }
    }

    const handleGoToSignInButton = () => {
        navigation.navigate("Sign In");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.bgSignUpContainer}>
                <Image
                    source={AreaLogo}
                    style={[styles.areaLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
                />
                <View style={styles.SignUpContainer}>
                    <Text style={styles.SignUpTitle}>Sign Up</Text>
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
                    <CustomerInput
                        placeholder="Confirmation Password"
                        value={repeatPassword}
                        setValue={setRepeatPassword}
                        secureTextEntry={true}
                    />
                    <CustomerButton
                        text="Get started"
                        onPress={handleSignInButton}
                        bgColor={"#666"}
                        fgColor={"white"}
                    />
                    <OrLine />
                    <SocialButton />
                    <CustomerButton
                        text="Already have an account ? Sign in here"
                        onPress={handleGoToSignInButton}
                        type="TERTIARY"
                        bgColor={""}
                        fgColor={""}
                    />
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    bgSignUpContainer: {
        marginTop: 20,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#F5F5F5',
    },
    SignUpContainer: {
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
    SignUpTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
})

export default SignUp;
