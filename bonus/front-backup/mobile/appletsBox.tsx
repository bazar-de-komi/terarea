import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity, Alert } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomButton from "../../components/CustomButton/customButton";
import Header from '../../components/Header/header';
import BackButton from "../../components/BackButton/backButton";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const AppletsScreen = ({ route }) => {
    const { applet } = route.params;
    const navigation = useNavigation();
    const [connectText, setConnectText] = useState("Connect");

    useEffect(() => {
        const isUserConnected = async () => {
            const token: string = await getValue("token");
            const response = await queries.get("/api/v1/user_applets", {}, token);
            const applets = response.msg;

            applets.forEach(userApplet => {
                if (userApplet.id === applet.id) {
                    setConnectText("Disconnect");
                    return;
                }
            });
        }
        isUserConnected();
    }, []);

    const handleConnectOrDisconnectButton = async () => {
        const token: string = await getValue("token");
        if (connectText === "Connect") {
            try {
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
        } else {
            try {
                let path: string = "/api/v1/disconnect_applet/";
                const idStr: string = applet.id.toString();
                path += idStr;
                await queries.post(path, {}, token);
                Alert.alert("You're disconnected successfully to the applet.");
                navigation.navigate('All');
            } catch (error) {
                console.error(error);
                Alert.alert("Failed to disconnect with the applet.");
            }
        }
    }

    const handleGoBackButton = () => {
        navigation.goBack();
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Header />
                <BackButton
                    text="<"
                    onPress={handleGoBackButton}
                />
                <Text style={styles.homeTitle}>
                    {applet.name}
                </Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>
                    {applet.description}
                </Text>
            </View>
            <View style={styles.connectStyle}>
                <CustomButton
                    text={connectText}
                    onPress={handleConnectOrDisconnectButton}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                />
            </View>
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
