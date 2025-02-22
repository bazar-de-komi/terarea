import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native'
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomInput from "../../components/CustomInput/customInput";
import Header from "../../components/Header/header";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServicesAction = () => {
    const navigation = useNavigation();
    const route = useRoute();

    const [actions, setActions] = useState([]);
    const [search, setSearch] = useState("");

    const { service, trigger } = route.params || {};

    const goBack = () => {
        navigation.goBack();
    }

    useEffect(() => {
        const fetchActions = async () => {
            if (!service || !service.id) {
                console.error("Aucun service sélectionné !");
                return;
            }

            try {
                const token = await getValue("token");
                const response = await queries.get(`/api/v1/reactions/service/${service.id}`, {}, token);
                if (response.resp === "success") {
                    setActions(response.msg);
                }
            } catch (error) {
                console.error("Error fetching actions:", error);
            }
        };
        fetchActions();
    }, [service]);

    const handleActionSelection = (service: any, action: any, trigger: any) => {
        navigation.navigate("Create action", { service, action, trigger });
    };

    const filteredActions = actions.filter(action => {
        if (!search.trim()) return true;

        const searchWords = search.toLowerCase().split(/\s+/).filter(word => word.length > 0);

        const matchesName = searchWords.some(word =>
            action.json.name?.toLowerCase().split(/\s+/).some((nameWord: any) => nameWord.includes(word))
        );

        const matchesDescription = searchWords.some(word =>
            action.json.description?.toLowerCase().split(/\s+/).some((descWord: any) => descWord.includes(word))
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
                {service ? `Choose an action for ${service.name}` : "Choose an action"}
            </Text>

            <View style={styles.searchContainer}>
                <CustomInput
                    value={search}
                    setValue={setSearch}
                    placeholder="Search Services"
                    secureTextEntry={false}
                />
            </View>

            {filteredActions.length > 0 ? (
                filteredActions.map(action => (
                    <AppletAndServiceBox
                        key={action.id}
                        title={action.json.name || "Unknown Trigger"}
                        description={action.json.description || "No description available"}
                        bgColor={"#f39c12"}
                        onPress={() => handleActionSelection(service, action, trigger)}
                    />
                ))
            ) : (
                <Text style={styles.noResults}>No actions found</Text>
            )}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 50,
        textAlign: "center"
    },
    searchContainer: {
        alignItems: 'center',
        marginBottom: 20,
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
})

export default ChooseServicesAction
