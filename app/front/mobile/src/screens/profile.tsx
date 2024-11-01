import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, Image} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../components/CustomersInput/CustomerInput";
import BackButton from "../components/BackButton/backButton";
import SocialAuthButton from "../components/SocialAuthButton";

import Header from "../components/Header/header";

import ProfileLogo from "../../assets/profilLogo.png";

const Profile = () => {
    const Navigation = useNavigation();

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header/>   
            <Text style={styles.homeTitle}>Account Setting</Text>
            <BackButton
                text={">"}
                onPress={""}
            />
            <Text style={styles.homeProfileTxt}>Profile</Text>
            <Image
                source={ProfileLogo}
                style={styles.profileLogo}
            />
            <Text style={styles.personalizeTxt}>Personalize your account by linking a profil from another service.</Text>
            <Text style={styles.homeAccountTitle}>Account</Text>
            <Text style={styles.optionTitle}>Username</Text>
            <View style={styles.homeNavigation}>
            </View>
            <View style={styles.searchBar}>
                <CustomerInput
                placeholder="UsernameData"
                />
            </View>
            <Text style={styles.optionTitle}>Password</Text>
            <View style={styles.searchBar}>
                <CustomerInput
                placeholder="PasswordData"
                />
            </View>
            <Text style={styles.optionTitle}>Email</Text>
            <View style={styles.searchBar}>
                <CustomerInput
                placeholder="EmailData"
                />
            </View>
            <Text style={styles.homeTitle}>Linked accounts</Text>
            <SocialAuthButton />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 10,
        marginLeft: 90,
        alignItems: 'center',
    },
    homeAccountTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 10,
        marginLeft: 140,
        alignItems: 'center',
    },
    homeProfileTxt: {
        fontSize: 24,
        fontWeight: 'bold',
        marginLeft: 50,
    },
    personalizeTxt: {
        fontSize: 18,
        marginLeft: 150,
        bottom: 50,
    },
    optionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginLeft: 50,
    },
    profileLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: 60,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
    },
    searchBar: {
        marginBottom: 10,
        width: '100%',
        left: 50,
    },
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
});

export default Profile;