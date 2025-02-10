import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ScrollView, ActivityIndicator} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import BackButton from "../../components/BackButton/backButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const ServicesScreen = () => {
    const Navigation = useNavigation();
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('https://ton-backend.com/api/services')
            .then(response => response.json())
            .then(data => {
                setServices(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Erreur lors de la récupération des services:", error);
                setLoading(false);
            });
    }, []);

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
                <Text style={styles.description}>5-Minute Crafts</Text>
            </View>
            <View style={styles.connectStyle}>
                    <CustomerButton
                    text="Connect"
                    onPress={signUp}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                    />
                </View>
            <Text style={styles.descriptionSericesAfterConnectButton}>Receive a weekly email digest of all new videos for the "5-Minyes Crafts" Youtube channel</Text> */}
            {loading ? (
                    <ActivityIndicator size="large" color="#fff" />
                ) : (
                    services.map(service => (
                        <View key={service.id} style={styles.serviceContainer}>
                            <Text style={styles.serviceTitle}>{service.name}</Text>
                            <Text style={styles.serviceDescription}>{service.description}</Text>
                            <CustomerButton
                                text="Voir plus"
                                onPress={() => serviceDetails(service.id)}
                                type="PRIMARY"
                            />
                        </View>
                    ))
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
    descriptionSericesAfterConnectButton: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    description: {
        fontSize: 20,
        margin: 30,
        color: 'white',
        // fontFamily: 'font',
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    connectStyle: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default ServicesScreen