import React, { useState } from "react";
import { View, Text, Image, StyleSheet, useWindowDimensions, ScrollView, Alert} from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from 'axios';
import { queries } from "../../../../back-endConnection/querier";

import CustomerInput from "../../../components/CustomersInput";
import CustomerButton from '../../../components/CustomerButton';
import SocialLogo from '../../../components/SocialAuthButton/socialAuthButton';

import AreaLogo from '../../../../assets/authenticationLogo/AreaLogo.png';

const SignIn = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { height } = useWindowDimensions() ;
    const navigation = useNavigation();

    const SignInPressed = () => {
        navigation.navigate('Home', { page: 'Home'});
        // setIsSubmitting(true);
        // const account = {
        //     email: email,
        //     password: password,
        // };
        // try {
        //     const result = await queries.post("/login", account);

        //     if (result && result.detail) {
        //         localStorage.setItem('token', result.detail);
        //         navigation.navigate("Home");
        //     } else {
        //         setError("Identifiant or password incorrect");
        //     }
        // } catch (error) {
        //     console.error("Sign error: ", error);
        //     setError("Error to connecte. Please check your id or your password");
        // } finally {
        //     setIsSubmitting(false);
        // }
    }

    const forgotPasswordPressed = () => {
        navigation.navigate("Forgot password");
    }

    const loginPressed = () => {
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
                        text="Forgot your password ?"
                        onPress={forgotPasswordPressed}
                        type="TERTIARY"
                        bgColor=""
                        fgColor="black"
                        icon=""
                    />
                    <CustomerButton
                    text="Get started"
                    onPress={SignInPressed}
                    bgColor={"black"}
                    fgColor={"white"}
                    icon=""
                    />
                    <SocialLogo/>
                    <CustomerButton
                        text="New to IFTTT ? Sign up here"
                        onPress={loginPressed}
                        type="TERTIARY"
                        bgColor=""
                        fgColor="black"
                        icon=""
                    />
                </View>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    backgroundContainer: {
        top: 20,
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
        marginBottom: 60,
    },
    headerText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
});

export default SignIn;
