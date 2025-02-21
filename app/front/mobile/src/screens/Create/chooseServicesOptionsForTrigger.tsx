import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomInput from "../../components/CustomInput/customInput";
import Header from "../../components/Header/header";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServices = () => {
    const navigation = useNavigation();
    const [services, setServices] = useState([]);
    const [search, setSearch] = useState("");

    const goBack = () => {
        navigation.goBack();
    }

    useEffect(() => {
        const fetchServices = async () => {
            try {
                const token = await getValue("token");
                const response = await queries.get("/api/v1/triggers_services", {}, token);

                if (response.resp === "success") {
                    setServices(response.msg);
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des services :", error);
            }
        };
        fetchServices();
    }, []);

    const handleServiceClick = (service: any) => {
        navigation.navigate("Choose services trigger", { service });
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <TouchableOpacity style={styles.backButtonContainer} onPress={goBack}>
                <Text style={styles.backButtonText}>
                    Back
                </Text>
            </TouchableOpacity>
            <Text style={styles.homeTitle}>Choose a service</Text>

            <View style={styles.searchContainer}>
                <CustomInput
                    value={search}
                    setValue={setSearch}
                    placeholder="Search Services"
                    secureTextEntry={false}
                />
            </View>

            {services
                .filter(service => {
                    if (!search.trim()) return true;

                    const searchWords = search.toLowerCase().split(/\s+/).filter(word => word.length > 0);

                    const matchesName = searchWords.some(word =>
                        service.name?.toLowerCase().split(/\s+/).some((nameWord: any) => nameWord.includes(word))
                    );

                    const matchesDescription = searchWords.some(word =>
                        service.description?.toLowerCase().split(/\s+/).some(descWord => descWord.includes(word))
                    );
                    return matchesName || matchesDescription;
                })
                .map((service) => (
                    <AppletAndServiceBox
                        key={service.id}
                        title={service.name || "Unknown Service"}
                        description={service.description || "No description available"}
                        bgColor={service.colour || "gray"}
                        onPress={() => handleServiceClick(service)}
                    />
                ))}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        marginTop: 50,
        marginBottom: 20,
        textAlign: 'center'
    },
    searchContainer: {
        alignItems: 'center',
        marginBottom: 20
    },
    backButtonContainer: {
        marginTop: 10,
        marginLeft: 20,
        marginRight: 'auto',
        textAlign: 'center',
        paddingHorizontal: 10,
        paddingVertical: 10,
        borderRadius: 25,
        borderColor: 'black',
        borderWidth: 2
    },
    backButtonText: {
        fontWeight: 'bold'
    }
})

export default ChooseServices
