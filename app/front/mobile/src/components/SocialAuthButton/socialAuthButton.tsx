import React from "react";
import { View, Image, StyleSheet, Alert } from 'react-native';
import { useNavigation } from "@react-navigation/native";

import CustomButton from "../CustomButton/customButton";

import GoogleLogo from '../../../assets/authenticationLogo/google.png';
import githubLogo from '../../../assets/authenticationLogo/githubLogo.png';
import DiscordLogo from '../../../assets/authenticationLogo/discord.png';
import SpotifyLogo from '../../../assets/authenticationLogo/spotify.png';

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
            <CustomButton
                text="Continue with Google"
                onPress={SignInGoogle}
                bgColor="white"
                fgColor="black"
                icon={<Image source={GoogleLogo} style={styles.logo} />}
                type=""
            />
            <CustomButton
                text="Continue with GitHub"
                onPress={SignInGithub}
                bgColor="#181717"
                fgColor="white"
                icon={<Image source={githubLogo} style={styles.logo} />}
                type=""
            />
            <CustomButton
                text="Continue with Discord"
                onPress={SignInDiscord}
                bgColor="#5865F2"
                fgColor="white"
                icon={<Image source={DiscordLogo} style={styles.discordLogo} />}
                type=""
            />
            <CustomButton
                text="Continue with Spotify"
                onPress={SignInSpotify}
                bgColor="#1DB954"
                fgColor="white"
                icon={<Image source={SpotifyLogo} style={styles.logo} />}
                type=""
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
    discordLogo: {
        width: 30,
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
