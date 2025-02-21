import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomerInput from "../../components/CustomersInput";
import BackButton from "../../components/BackButton/backButton";

import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ChooseServicesAction = () => {
    const Navigation = useNavigation();
    const route = useRoute();

    const AppletsHome = () => {
        Navigation.navigate("Applets");
    }

    const [actions, setActions] = useState([]);
    const [search, setSearch] = useState("");

    const { service, trigger } = route.params || {};

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
                    console.log("Response: ", response.msg);
                    setActions(response.msg);
                    console.log(response.msg[0].json);
                } else {
                    console.error("La réponse de l'API ne contient pas la bonne structure.");
                    setActions([]);
                }
            } catch (error) {
                console.error("Error fetching actions:", error);
                setActions([]);
            }
        };

        fetchActions();
    }, [service]);

    const handleActionSelection = (service, action, trigger) => {
        Navigation.navigate("Create action", { service, action, trigger });
    };

    const filteredActions = actions.filter(action =>
        action.json.name && action.json.name.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <BackButton 
            text={"back"}
            onPress={AppletsHome}
            />
            <Text style={styles.homeTitle}>
                {service ? `Choose an action for ${service.name}` : "Choose an action"}
            </Text>

            <View style={styles.searchContainer}>
                <CustomerInput
                    placeholder="Search Services"
                    style={styles.searchInput}
                    onChangeText={setSearch}
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

export default ChooseServicesAction
