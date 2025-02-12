import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ScrollView, ActivityIndicator} from 'react-native'
import { useNavigation, useRoute } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import BackButton from "../../components/BackButton/backButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const ServicesScreen = () => {
    const Navigation = useNavigation();
    const route = useRoute();
    const { applet_id } = route.params || {};

    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchServices = async () => {
            if (!applet_id) {
                console.error("Aucun applet_id fourni !");
                setLoading(false);
                return;
            }

            try {
                const response = await fetch(`https://ton-backend.com/api/v1/my_applet/${applet_id}`);
                if (!response.ok) {
                    throw new Error(`Erreur HTTP ! Statut : ${response.status}`);
                }
                const data = await response.json();
                setServices(data);
            } catch (error) {
                console.error("Erreur lors de la récupération des services:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchServices();
    }, [applet_id]);
    
    const signUp = () => {
        Navigation.navigate('All');
    }

    const serviceDetails = () => {
        Navigation.navigate('Service details')
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
                onPress={serviceDetails}
                />

                {/* <Text style={styles.homeTitle}>Receive a weekly email digest of all new videos for the "5-Minyes Crafts" Youtube channel</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>5-Minute Crafts</Text> */}
            {loading ? (
                    <ActivityIndicator size="large" color="#fff" />
                ) : (
                    services.length > 0 ? (
                        services.map(service => (
                            <View key={service.json.id} style={styles.serviceContainer}>
                                <Text style={styles.serviceTitle}>{service.json.name}</Text>
                                <Text style={styles.serviceDescription}>{service.json.description}</Text>
                                <CustomerButton
                                    text="Voir plus"
                                    onPress={() => serviceDetails(service.json.id)}
                                    type="PRIMARY"
                                />
                            </View>
                        ))
                    ) : (
                        <Text style={styles.noServiceText}>Aucun service disponible.</Text>
                    )
                )}
            </View>

            {/* <View style={styles.connectStyle}>
                    <CustomerButton
                    text="Connect"
                    onPress={signUp}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                    />
                </View> */}
            {/* <Text style={styles.descriptionSericesAfterConnectButton}>Receive a weekly email digest of all new videos for the "5-Minyes Crafts" Youtube channel</Text> */}
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