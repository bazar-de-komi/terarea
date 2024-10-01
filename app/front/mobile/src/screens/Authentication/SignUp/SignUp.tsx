import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView} from "react-native";
// import IftttLogo from '../../../assets/authenticationLogo/font-style.png';
import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from '../../../components/CustomerButton/CustomerButton';
// import GoogleLogo from '../../../assets/authenticationLogo/google.png';
// import GoogleLogo from '../../../assets/authenticationLogo/google.png';
import GoogleLogo from '../../../../assets/authenticationLogo/google.png';

import { useNavigation } from "@react-navigation/native";

const SignUp = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');

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
                <Image source={GoogleLogo} style={styles.logo} />
                <CustomerButton
                text="Sign in with Google"
                onPress={SignInGoogle}
                bgColor="#FAE9EA"
                fgColor="#DD4D44"
                />
            {/* </View> */}
            <CustomerButton text="Sign in with GitHub" onPress={SignInGithub} bgColor="#e3e3e3" fgColor="#363636"/>

            <CustomerButton
            text="Already on IFTTT ? Sign in here"
            onPress={loginPressed}
            type="TERTIARY"
            bgColor={""}
            fgColor={""}
            />

        </View>
    </ScrollView>
    );
};

const styles = StyleSheet.create({
    SignUpContainer: {
        alignItems: 'center',
        padding: 20,
    },
    IftttLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 200,
    },
    logoButtonContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        width: '80%',
        borderRadius: 5,
        padding: 10,
        marginVertical: 5,
    },
    logo: {
        right: 80,
        top: 40,
        width: 24,
        height: 24,
        marginRight: 10,
    },
    SignUpTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#051C60',
        margin: 10,
    },
})

export default SignUp;