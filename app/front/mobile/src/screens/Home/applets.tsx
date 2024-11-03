import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from '../../components/Header/header';
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const Applets = () => {
    const navigation = useNavigation();
    const [applets, setApplets] = useState([]);
    const [tags, setTags] = useState("");

    const handleAllButton = () => {
        navigation.navigate("All");
    };

    const handleAppletsButton = () => {
        navigation.navigate("Applets");
    };

    const handleServicesButton = () => {
        navigation.navigate("Services");
    };

    const handleAppletButton = async (applet: any) => {
        navigation.navigate("Applet screen", { applet: applet });
    };

    useEffect(() => {
        const getApplets = async () => {
            try {
                const token = await getValue("token");
                const getServicesResponse = await queries.get("/api/v1/applets", {}, token);
                setApplets(getServicesResponse.msg);
            } catch (error) {
                console.error(error);
            }
        };
        getApplets();
    }, []);

    useEffect(() => {
        const getAppletsByTags = async () => {
            try {
                const token = await getValue("token");
                if (tags === "") {
                    const getAppletsResponse = await queries.get("/api/v1/applets", {}, token);
                    setApplets(getAppletsResponse.msg);
                } else {
                    const noSpaceTags = tags.replaceAll(" ", ":");
                    console.log("NoSpaceTags", noSpaceTags);
                    let path = "/api/v1/applets/";
                    path += noSpaceTags;
                    const getAppletsResponse = await queries.get(path, {}, token);
                    setApplets(getAppletsResponse.msg);
                }
            } catch (error) {
                console.error(error);
                setApplets([]);
            }
        }
        getAppletsByTags();
    }, [tags]);

    // const appletsData = [
    //     {
    //         title: "Get the weather forecast every dat at 7:00 AM",
    //         description: "Weather Underground",
    //         bgColor: "orange",
    //     },
    //     {
    //         title: "Quickly create events in Google Calendar",
    //         description: "Google",
    //         bgColor: "blue",
    //     },
    //     {
    //         title: "Track your fitness goals daily",
    //         description: "Fitbit",
    //         bgColor: "green",
    //     },
    // ];

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <Text style={styles.homeTitle}>Explore</Text>
            <View style={styles.homeNavigation}>
                <CustomerButton
                    text="All"
                    onPress={handleAllButton}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                />
                <CustomerButton
                    text="Applets"
                    onPress={handleAppletsButton}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={"blue"}
                />
                <CustomerButton
                    text="Services"
                    onPress={handleServicesButton}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                />
            </View>
            <View style={styles.searchBar}>
                <CustomerInput
                    value={tags}
                    setValue={setTags}
                    placeholder="Search applets"
                />
            </View>
            {
                applets.map((applet) => (
                    <AppletAndServiceBox
                        key={applet.id}
                        title={applet.name}
                        description={applet.description}
                        author={applet.author}
                        user_nb={applet.frequency}
                        bgColor={applet.colour}
                        onPress={() => handleAppletButton(applet)}
                    />
                ))
            }
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        marginLeft: 150,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    searchBar: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default Applets
