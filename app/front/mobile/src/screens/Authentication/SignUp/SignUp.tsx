import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from '../../../components/CustomerButton/CustomerButton';
import GoogleLogo from '../../../../assets/authenticationLogo/google.png';
import IftttLogo from '../../../../assets/authenticationLogo/font-style.png';
import GithubLogo from '../../../../assets/authenticationLogo/githubLogo.png';

import { useNavigation } from "@react-navigation/native";

const SignUp = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');

    const { height } = useWindowDimensions();

    const navigation = useNavigation();

    const SignInPressed = () => {
        // console.warn("Sign Up");

        navigation.navigate('Home');
    }

    const SignInGoogle = () => {
        console.warn("Sing In Google");
    }

    const SignInGithub = () => {
        console.warn("Sing In Github");
    }

    const loginPressed = () => {
        // console.warn("Log in");
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgSignUpContainer}>
            <Image source={IftttLogo} style={[styles.IftttLogo, { height: height * 0.1}]} resizeMode="contain" />
                <View style={styles.SignUpContainer}>
                    <Text style={styles.SignUpTitle}>Sign Up</Text>
                    <CustomerInput
                    placeholder="Username"
                    value={username}
                    setValue={setUsername}
                    secureTextEntry={false}
                    />
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
                    placeholder="Repeat Password"
                    value={repeatPassword}
                    setValue={setRepeatPassword}
                    secureTextEntry={true}
                    />
                    <CustomerButton text="Get started" onPress={SignInPressed} bgColor={""} fgColor={""}/>
                    {/* <View style={styles.logoButtonContainer}> */}
                        {/* <Image source={GoogleLogo} style={styles.logo} />
                        <CustomerButton
                        text="Sign in with Google"
                        onPress={SignInGoogle}
                        bgColor="#FAE9EA"
                        fgColor="#DD4D44"
                        /> */}
                    {/* </View> */}
                    {/* <CustomerButton text="Sign in with GitHub" onPress={SignInGithub} bgColor="#e3e3e3" fgColor="#363636"/> */}
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
                        icon={<Image source={GithubLogo} style={styles.logo} />}
                    />
                    <CustomerButton
                    text="Already on IFTTT ? Sign in here"
                    onPress={loginPressed}
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
        top: 20,
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
    IftttLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 100,
        marginBottom: 60,
    },
    logo: {
        width: 24,
        height: 24,
        marginRight: 10,
    },
    SignUpTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
})

export default SignUp;