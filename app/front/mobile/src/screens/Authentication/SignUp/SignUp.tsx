import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView, useWindowDimensions} from "react-native";
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from '../../../components/CustomerButton/CustomerButton';
import SocialButton from '../../../components/SocialAuthButton/socialAuthButton';

import IftttLogo from '../../../../assets/authenticationLogo/font-style.png';

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

    const loginPressed = () => {
        // console.warn("Log in");
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.bgSignUpContainer}>
            <Image 
                source={IftttLogo}
                style={[styles.IftttLogo, { height: height * 0.1}]}
                resizeMode="contain"
            />
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
                    placeholder="Confirmation Password"
                    value={repeatPassword}
                    setValue={setRepeatPassword}
                    secureTextEntry={true}
                    />
                    <CustomerButton
                        text="Get started"
                        onPress={SignInPressed}
                        bgColor={""}
                        fgColor={""}
                    />
                    <SocialButton/>
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
    SignUpTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
})

export default SignUp;