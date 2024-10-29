import React from "react";
import {View, Image, StyleSheet, Text} from 'react-native';

import CustomerButton from "../CustomerButton";
import OrLine from "./OrLine";

import GoogleLogo from '../../../assets/authenticationLogo/google.png';
import githubLogo from '../../../assets/authenticationLogo/githubLogo.png';

const SocialAuthButton = () => {
    const SignInGoogle = () => {
        console.warn("Sign In Google");
    }

    const SignInGithub = () => {
        console.warn("Sign In Github");
    }

    const SignInDiscord = () => {
        console.warn("Sign In Discord");
    }

    const SignInSpotify = () => {
        console.warn("Sign In Spotify");
    }

    return (
        <View style={styles.container}>
            <OrLine/>
            <CustomerButton
                text="Sign in with Google"
                onPress={SignInGoogle}
                bgColor="white"
                fgColor="black"
                icon={<Image source={GoogleLogo} style={styles.logo} />}
                type=""
            />
            <CustomerButton
                text="Sign in with GitHub"
                onPress={SignInGithub}
                bgColor="#303030"
                fgColor="white"
                icon={<Image source={githubLogo} style={styles.logo} />}
            />
            <CustomerButton
                text="Sign in with Discord"
                onPress={SignInDiscord}
                bgColor="purple"
                fgColor="white"
                icon={<Image source={githubLogo} style={styles.logo} />}
            />
            <CustomerButton
                text="Sign in with Spotify"
                onPress={SignInSpotify}
                bgColor="green"
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

export default SocialAuthButton;