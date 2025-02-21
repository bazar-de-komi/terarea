import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ScrollView, ActivityIndicator } from 'react-native'
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomButton from "../../components/CustomButton";
import BackButton from "../../components/BackButton/backButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const ServicesScreen = () => {
    const Navigation = useNavigation();
    const route = useRoute();
    const { applet_id } = route.params || {};

    const [applet, setApplet] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchServices = async () => {
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

        fetchServices();
    }, [applet_id]);

    const goBack = () => {
        Navigation.navigate('Applets');
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={ProfilLogo}
                    style={styles.profilLogo}
                />
                <BackButton
                    text="<"
                    onPress={goBack}
                />

                {loading ? (
                    <ActivityIndicator size="large" color="#fff" />
                ) : (
                    <View>
                        <Text style={styles.serviceTitle}>{applet.name}</Text>
                        <Text style={styles.serviceDescription}>{applet.description}</Text>
                    </View>
                )}
            </View>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    backContainer: {
        marginTop: 30,
        backgroundColor: "green",
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
        height: 500,
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
        color: 'white',
        // fontFamily: 'arial',
    },
    serviceContainer: {
        backgroundColor: '#fff',
        padding: 15,
        marginVertical: 10,
        borderRadius: 10,
        width: '90%',
    },
    serviceTitle: {
        fontSize: 22,
        fontWeight: 'bold',
        color: 'black',
    },
    serviceDescription: {
        fontSize: 16,
        marginBottom: 10,
        color: 'gray',
    },
    noServiceText: {
        fontSize: 18,
        color: 'white',
        marginTop: 20,
    },
})

export default ServicesScreen
