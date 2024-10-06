import React from "react";
import {View, Image, StyleSheet, Text} from 'react-native';
import CustomerButton from "../CustomerButton";

import GoogleLogo from '../../../assets/authenticationLogo/google.png';
import githubLogo from '../../../assets/authenticationLogo/githubLogo.png';

const SocialSingInButton = () => {
    const SignInGoogle = () => {
        console.warn("Sign In Google");
    }

    const SignInGithub = () => {
        console.warn("Sign In Github");
    }

    return (
        <View style={styles.container}>
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
        </View>
    );
};

const styles = StyleSheet.create({
    logo: {
        width: 24,
        height: 24,
        marginRight: 10,
    },
    container: {
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        marginVertical: 10,
    }
});

export default SocialSingInButton;