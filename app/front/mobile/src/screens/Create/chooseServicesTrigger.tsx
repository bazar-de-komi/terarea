
import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomerInput from "../../components/CustomersInput";
import BackButton from "../../components/BackButton/backButton";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServicesTrigger = () => {
    const Navigation = useNavigation();
    const route = useRoute();
    
    const [triggers, setTriggers] = useState([]);
    const [search, setSearch] = useState("");
    
    const { service } = route.params || {};
    
    useEffect(() => {
        const fetchTriggers = async () => {
            if (!service || !service.id) {
                console.error("Aucun service sélectionné !");
                return;
            }

            try {
                const token = await getValue("token");
                const response = await queries.get(`/api/v1/triggers/service/${service.id}`, {}, token);
                if (response.resp === "success") {
                    console.log("Response:", response.msg);
                    setTriggers(response.msg);
                    console.log(response.msg[0].json);
                } else {
                    console.error("La réponse de l'API ne contient pas la bonne structure.");
                    setTriggers([]);
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des triggers :", error);
                setTriggers([]);
            }
        };
        
        fetchTriggers();
    }, [service]);

    const handleTriggerClick = ( service, trigger) => {
        Navigation.navigate("Date time trigger", { service, trigger });
    };

    const filteredTriggers = triggers.filter(trigger =>
        trigger.json.name && trigger.json.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <BackButton 
                text={"back"}
                onPress={() => Navigation.goBack()}
            />
            <Text style={styles.homeTitle}>
                {service ? `Choose a trigger for ${service.name}` : "Choose a trigger"}
            </Text>

            <View style={styles.searchContainer}>
                <CustomerInput
                    placeholder="Search Triggers"
                    style={styles.searchInput}
                    onChangeText={setSearch}
                />
            </View>

            {filteredTriggers.length > 0 ? (
                filteredTriggers.map(trigger => (
                    <AppletAndServiceBox
                        key={trigger.id}
                        title={trigger.json.name || "Unknown Trigger"}
                        description={trigger.json.description || "No description available"}
                        bgColor={"#f39c12"}
                        onPress={() => handleTriggerClick(service, trigger)}
                    />
                ))
            ) : (
                <Text style={styles.noResults}>No triggers found</Text>
            )}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 100,
        textAlign: "center",
    },
    searchContainer: {
        alignItems: 'center',
        marginVertical: 10,
    },
    searchInput: {
        width: '80%',
    },
    noResults: {
        textAlign: 'center',
        fontSize: 18,
        marginVertical: 20,
        color: "gray",
    }
});

export default ChooseServicesTrigger;
