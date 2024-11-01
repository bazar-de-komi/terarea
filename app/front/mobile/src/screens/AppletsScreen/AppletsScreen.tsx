import React from "react";
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity, Alert } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import Header from '../../components/Header/header';
import BackButton from "../../components/BackButton/backButton";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const AppletsScreen = ({ route }) => {
    const { applet } = route.params;
    const navigation = useNavigation();

    const handleConnectButton = async () => {
        try {
            const token: string = await getValue("token");
            let path: string = "/api/v1/connect_applet/";
            const idStr: string = applet.id.toString();
            path += idStr;
            await queries.post(path, {}, token);
            Alert.alert("You're connected successfully to the applet.");
            navigation.navigate('All');
        } catch (error) {
            console.error(error);
            Alert.alert("Failed to connect with the applet.");
        }
    }

    const handleGoBackButton = () => {
        navigation.goBack();
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Header />
                {/* <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={ProfilLogo}
                    style={styles.profilLogo}
                />
                <View style={styles.backStyle}>
                    <CustomerButton
                        text='<'
                        onPress={callApplets}
                        type="TERTIARY"
                        bgColor={""}
                        fgColor={""}
                    />
                </View> */}
                <BackButton
                    text="<"
                    onPress={handleGoBackButton}
                />
                <Text style={styles.homeTitle}>
                    {applet.name}
                    {/* 5-Minute Crafts integrations */}
                </Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>
                    {applet.description}
                    {/* The 5-Minute Crafts Youtube channel is a */}
                </Text>
            </View>
            <View style={styles.connectStyle}>
                <CustomerButton
                    text="Connect"
                    onPress={handleConnectButton}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                />
            </View>
            {/* <Text style={styles.homeTitle}>Get appletsScreensed with any Applet</Text> */}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    backContainer: {
        marginTop: 30,
        backgroundColor: "orange",
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
        height: 500,
    },
    areaLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: -250,
    },
    profilLogo: {
        maxHeight: 50,
        marginTop: -50,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        color: 'white',
    },
    descriptionAppletsAfterConnectButton: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    description: {
        fontSize: 20,
        margin: 30,
        color: 'white',
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    connectStyle: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
    backStyle: {
        marginBottom: 40,
        width: '180%',
        alignSelf: 'center',
        fontWeight: 'bold',
        fontSize: 35,
        color: "green",
    },
})

export default AppletsScreen
