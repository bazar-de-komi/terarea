import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native'
import { useRoute } from "@react-navigation/native";

import CustomButton from "../../components/CustomButton";
import Header from "../../components/Header/header";

import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const AppletInformation = () => {
    const route = useRoute();
    const { applet_id } = route.params || {};

    const [applet, setApplet] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchApplet = async () => {
            if (!applet_id) {
                console.error("Aucun applet_id fourni !");
                setLoading(false);
                return;
            }

            try {
                const token = await getValue("token");
                const response = await queries.get(`/api/v1/my_applet/${applet_id}`, {}, token);
                if (response.resp === "success") {
                    setApplet(response.msg);
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des services:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchApplet();
    }, [applet_id]);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            {loading ? (
                <ActivityIndicator size="large" color="#fff" />
            ) : (
                <View style={{ ...styles.mainContainer, backgroundColor: applet?.colour }}>
                    <Header />
                    <View>
                        <Text style={styles.appletTitle}>{applet?.name}</Text>
                        <Text style={styles.appletDescription}>{applet?.description}</Text>
                    </View>
                </View>
            )}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        marginTop: 30,
        borderRadius: 10,
        alignItems: 'center',
        padding: 5
    },
    appletTitle: {
        fontSize: 30,
        fontWeight: 'bold',
        color: 'black',
        textAlign: 'center',
        marginTop: 30
    },
    appletDescription: {
        fontSize: 18,
        marginTop: 10,
        marginBottom: 20,
        color: 'gray',
        textAlign: 'center'
    }
})

export default AppletInformation;
