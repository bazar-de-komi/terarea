import React from "react";
import { View, Image, StyleSheet, Alert } from 'react-native';
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../CustomerButton";
import OrLine from "./OrLine";

import GoogleLogo from '../../../assets/authenticationLogo/google.png';
import githubLogo from '../../../assets/authenticationLogo/githubLogo.png';
import { queries } from "../../../back-endConnection/querier";
import { storeValue } from "../StoreData/storeData";

const SocialAuthButton = () => {
    const navigation = useNavigation();

    const SignInGoogle = async () => {
        try {
            const provider = {
                provider: "google"
            };
            const response = await queries.post("/api/v1/oauth/login", provider);
            let url: string = response.authorization_url;
            url = decodeURIComponent(url);
            await storeValue("authUrl", url);
            navigation.navigate("Oauth screen");
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to get the authorisation url.");
        };
    };

    const SignInGithub = async () => {
        try {
            const provider = {
                provider: "github"
            };
            const response = await queries.post("/api/v1/oauth/login", provider);
            let url: string = response.authorization_url;
            url = decodeURIComponent(url);
            await storeValue("authUrl", url);
            navigation.navigate("Oauth screen");
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to get the authorisation url.");
        };
    };

    const SignInDiscord = async () => {
        try {
            const provider = {
                provider: "discord"
            };
            const response = await queries.post("/api/v1/oauth/login", provider);
            console.log("Response:", response);
            let url: string = response.authorization_url;
            url = decodeURIComponent(url);
            await storeValue("authUrl", url);
            navigation.navigate("Oauth screen");
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to get the authorisation url.");
        };
    };

    const SignInSpotify = async () => {
        try {
            const provider = {
                provider: "spotify"
            };
            const response = await queries.post("/api/v1/oauth/login", provider);
            let url: string = response.authorization_url;
            url = decodeURIComponent(url);
            await storeValue("authUrl", url);
            navigation.navigate("Oauth screen");
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to get the authorisation url.");
        };
    };

    return (
        <View style={styles.container}>
            {/* <OrLine /> */}
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
