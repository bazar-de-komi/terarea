import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerInput from "../../components/CustomersInput";
import BackButton from "../../components/BackButton/backButton";

import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServices = () => {
    const Navigation = useNavigation();

    const AppletsHome = () => {
        Navigation.navigate("Applets");
    }

    const [services, setServices] = useState([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        const fetchServices = async () => {
            try {
                const token = await getValue("token");
                const response = await queries.get("/api/v1/triggers_services", {}, token);
                
                if (Array.isArray(response.msg)) {
                    setServices(response.msg);
                } else {
                    console.error("La réponse de l'API ne contient pas la bonne structure.");
                    setServices([]);
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des services :", error);
                setServices([]);
            }
        };
        fetchServices();
    }, []);
    
    const handleServiceClick = (service: any) => {
        Navigation.navigate("Choose services trigger", { service });
    };
    
    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <BackButton 
            text={"back"}
            onPress={AppletsHome}
            />
            <Text style={styles.homeTitle}>Choose a service</Text>

            <View style={styles.searchContainer}>
                <CustomerInput
                    placeholder="Search Services"
                    style={styles.searchInput}
                />
            </View>

        {services
            .filter(service => service && service.name && service.name.toLowerCase().includes(search.toLowerCase()))
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
        margin: 80,
        marginLeft: 100,
        width: 1000,
    },
    searchContainer: {
        alignItems: 'center',
        marginVertical: 10,
    },
    searchInput: {
        width: '80%',
    },
    section: {
        alignItems: 'center',
        marginVertical: 20,
    },
    ifThisContainer: {
        flexDirection: 'row',
        position: 'relative',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
    },
    ifThisButton: {
        width: 250,
        height: 50,
    },
    addButtonContainer: {
        position: 'absolute',
        right: 10,
        width: 60,
        borderRadius: 80,
    },
    addButton: {
        paddingHorizontal: 10,
        paddingVertical: 5,
    }
})

export default ChooseServices
