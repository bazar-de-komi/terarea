import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from '../../components/Header/header';
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const Services = () => {
    const navigation = useNavigation();
    const [services, setServices] = useState([]);
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

    const handleServicesDetailsButton = (service: any) => {
        navigation.navigate('Service details', { service: service });
    };

    useEffect(() => {
        const getServices = async () => {
            try {
                const token = await getValue("token");
                const getServicesResponse = await queries.get("/api/v1/services", {}, token);
                setServices(getServicesResponse.msg);
            } catch (error) {
                console.error(error);
            }
        };
        getServices();
    }, []);

    useEffect(() => {
        const getServicesByTags = async () => {
            try {
                const token = await getValue("token");
                if (tags === "") {
                    const getServicesResponse = await queries.get("/api/v1/services", {}, token);
                    setServices(getServicesResponse.msg);
                } else {
                    const noSpaceTags = tags.replaceAll(" ", ":");
                    console.log("NoSpaceTags", noSpaceTags);
                    let path = "/api/v1/services/";
                    path += noSpaceTags;
                    const getServicesResponse = await queries.get(path, {}, token);
                    setServices(getServicesResponse.msg);
                }
            } catch (error) {
                console.error(error);
                setServices([]);
            }
        }
        getServicesByTags();
    }, [tags]);

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
                    fgColor={""}
                />
                <CustomerButton
                    text="Services"
                    onPress={handleServicesButton}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={"blue"}
                />
            </View>
            <View style={styles.searchBar}>
                <CustomerInput
                    value={tags}
                    setValue={setTags}
                    placeholder="Search Applets or Services"
                />
            </View>
            {/* <View style={styles.searchServices}>
                <CustomerInput
                    placeholder="All services"
                />
            </View> */}
            {
                services.map((service) => (
                    <AppletAndServiceBox
                        key={service.id}
                        title={service.name}
                        bgColor={service.colour}
                        onPress={() => handleServicesDetailsButton(service)}
                    />
                ))
            }
        </ScrollView>
    );
};

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
        marginBottom: 10,
        width: '130%',
        alignSelf: 'center',
    },
    searchServices: {
        alignItems: 'center',
        marginBottom: 40,
        width: '100%',
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
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
});

export default Services;
