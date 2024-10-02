import React, { useState } from "react";
import { View, Text, Image, StyleSheet, useWindowDimensions, ScrollView } from "react-native";
import CustomerInput from "../../../components/CustomersInput";
import CustomerButton from '../../../components/CustomerButton';
import IftttLogo from '../../../../assets/authenticationLogo/font-style.png';
import GoogleLogo from '../../../../assets/authenticationLogo/google.png';
import githubLogo from '../../../../assets/authenticationLogo/githubLogo.png';
import { useNavigation } from "@react-navigation/native";

const SignIn = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const { height } = useWindowDimensions();
    const navigation = useNavigation();

    const SignInPressed = () => {
        navigation.navigate("Home");
    }

    const forgotPasswordPressed = () => {
        navigation.navigate("Forgot password");
    }

    const SignInGoogle = () => {
        console.warn("Sign In Google");
    }

    const SignInGithub = () => {
        console.warn("Sign In Github");
    }

    const loginPressed = () => {
        navigation.navigate("Sign Up");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backgroundContainer}>
                <Image
                    source={IftttLogo}
                    style={[styles.IftttLogo, { height: height * 0.1 }]}
                    resizeMode="contain"
                />
                <View style={styles.SignInContainer}>
                    <Text style={styles.headerText}>Log In</Text>
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
                    onPress={SignInPressed}
                    bgColor={"black"}
                    fgColor={"white"}
                    icon=""
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
                        text="Sign in with Google"
                        onPress={SignInGoogle}
                        bgColor="white"
                        fgColor="black"
                        icon={<Image source={GoogleLogo} style={styles.logo} />}
                    />
                    <CustomerButton
                        text="Sign in with GitHub"
                        onPress={SignInGithub}
                        bgColor="#303030"
                        fgColor="white"
                        icon={<Image source={githubLogo} style={styles.logo} />}
                    />
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
    //box:
    SignInContainer: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: '#e0d8d7',
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
    },
    IftttLogo: {
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
    logo: {
        width: 24,
        height: 24,
        marginRight: 10,
    },
});

export default SignIn;
