
import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomInput from "../../components/CustomInput/customInput";
import Header from "../../components/Header/header";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServicesTrigger = () => {
    const navigation = useNavigation();
    const route = useRoute();

    const [triggers, setTriggers] = useState([]);
    const [search, setSearch] = useState("");

    const { service } = route.params || {};

    const goBack = () => {
        navigation.goBack();
    }

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
                    setTriggers(response.msg);
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des triggers :", error);
            }
        };
        fetchTriggers();
    }, [service]);

    const handleTriggerClick = (service: any, trigger: any) => {
        navigation.navigate("Create trigger", { service, trigger });
    };

    const filteredTriggers = triggers.filter(trigger => {
        if (!search.trim()) return true;

        const searchWords = search.toLowerCase().split(/\s+/).filter(word => word.length > 0);

        const matchesName = searchWords.some(word =>
            trigger.json.name?.toLowerCase().split(/\s+/).some((nameWord: any) => nameWord.includes(word))
        );

        const matchesDescription = searchWords.some(word =>
            trigger.json.description?.toLowerCase().split(/\s+/).some((descWord: any) => descWord.includes(word))
        );
        return matchesName || matchesDescription;
    });

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <TouchableOpacity style={styles.backButtonContainer} onPress={goBack}>
                <Text style={styles.backButtonText}>
                    Back
                </Text>
            </TouchableOpacity>
            <Text style={styles.homeTitle}>
                {service ? `Choose a trigger for ${service.name}` : "Choose a trigger"}
            </Text>

            <View style={styles.searchContainer}>
                <CustomInput
                    value={search}
                    setValue={setSearch}
                    placeholder="Search Triggers"
                // secureTextEntry={false}
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
        margin: 50,
        textAlign: "center"
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
        borderWidth: 2,
    },
    backButtonText: {
        fontWeight: 'bold'
    },
    noResults: {
        textAlign: 'center',
        fontSize: 18,
        marginVertical: 20,
        color: "gray",
    }
});

export default ChooseServicesTrigger;
