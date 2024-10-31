import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from "../../components/Header/header";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";
import { queries } from "../../../back-endConnection/querier";
import { getValue, storeValue } from "../../components/StoreData/storeData";

const All = () => {
    const navigation = useNavigation();
    const [applets, setApplets] = useState([]);
    const [services, setServices] = useState([]);
    const [tags, setTags] = useState("");

    const allScreens = () => {
        navigation.navigate("All");
    }
    const appletsScreens = () => {
        navigation.navigate("Applets");
    }

    const servicesScreens = () => {
        navigation.navigate("Services");
    }

    const handleAppletPress = async (applet: any) => {
        await storeValue("applet", applet);
        navigation.navigate("Applet screen");
    }

    useEffect(() => {
        const getAppletsAndServices = async () => {
            try {
                const token = await getValue("token");
                const getAppletsResponse = await queries.get("/api/v1/applets", {}, token);
                setApplets(getAppletsResponse.msg);
                const getServicesResponse = await queries.get("/api/v1/services", {}, token);
                setServices(getServicesResponse.msg);
            } catch (error) {
                console.error(error);
            }
        }
        getAppletsAndServices();
    }, []);

    useEffect(() => {
        const getAppletsAndServicesByTags = async () => {
            try {
                const token = await getValue("token");
                if (tags === "") {
                    const getAppletsResponse = await queries.get("/api/v1/applets", {}, token);
                    setApplets(getAppletsResponse.msg);
                    const getServicesResponse = await queries.get("/api/v1/services", {}, token);
                    setServices(getServicesResponse);
                } else {
                    const noSpaceTags = tags.replaceAll(" ", ":");
                    let path = "/api/v1/applets_by_tag/";
                    path += noSpaceTags;
                    const getAppletsResponse = await queries.get(path, {}, token);
                    setApplets(getAppletsResponse.msg);
                    path = "/api/v1/services/tag/";
                    path += noSpaceTags;
                    const getServicesResponse = await queries.get(path, {}, token);
                    setServices(getServicesResponse.msg);
                }
            } catch (error) {
                console.error(error);
            }
        }
        getAppletsAndServicesByTags();
    }, [tags]);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <Text style={styles.homeTitle}>Explore</Text>
            <View style={styles.homeNavigation}>
                <CustomerButton
                    text="All"
                    onPress={allScreens}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={"blue"}
                />
                <CustomerButton
                    text="Applets"
                    onPress={appletsScreens}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                />
                <CustomerButton
                    text="Services"
                    onPress={servicesScreens}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                />
            </View>
            <View style={styles.searchBar}>
                <CustomerInput
                    value={tags}
                    setValue={setTags}
                    placeholder="Search Applets or Services"
                />
            </View>
            {
                applets.map((applet, index) => (
                    <AppletAndServiceBox
                        key={index}
                        title={applet.title}
                        description={applet.description}
                        author={applet.author}
                        user_nb={applet.frequency}
                        bgColor={applet.color}
                    // onPress={}
                    />
                ))
            }
            {
                services.map((service, index) => (
                    <AppletAndServiceBox
                        key={index}
                        title={service.title}
                        bgColor={service.color}
                    // onPress={}
                    />
                ))
            }
            {/* <AppletAndServiceBox
                title="How we automate tiktok"
                description="Learn how to use TEST"
                bgColor="#f54242"
            />
            <AppletAndServiceBox
                title="How we automate tiktok"
                description="Learn how to use TEST"
                bgColor="#f54242"
            /> */}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    headerContainer: {
        marginTop: 30,
        backgroundColor: '#e0d8d7',
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
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
    AppletAndServiceBox: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: '#e0d8d7',
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
    },
})

export default All
