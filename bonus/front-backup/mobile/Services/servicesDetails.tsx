import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomButton from "../../components/CustomButton/customButton";
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";
import BackButton from "../../components/BackButton/backButton";
import Header from '../../components/Header/header';
import { getValue } from "../../components/StoreData/storeData";
import { queries } from "../../../back-endConnection/querier";

const ServicesDetails = ({ route }) => {
    const { service } = route.params;
    const navigation = useNavigation();
    const [applets, setApplets] = useState([]);

    const handleGoBackButton = () => {
        navigation.goBack();
    }

    const handleAppletButton = async (applet: any) => {
        navigation.navigate("Applet screen", { applet: applet });
    };

    const handleCreateButton = () => {
        navigation.navigate('Create');
    };

    useEffect(() => {
        const getAppletsOfService = async () => {
            try {
                const token = await getValue("token");
                let path = "/api/v1/applets/";
                path += service.name;
                const getAppletsResponse = await queries.get(path, {}, token);
                setApplets(getAppletsResponse.msg);
            } catch (error) {
                console.error(error);
            }
        };
        getAppletsOfService();
    }, []);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Header />
                <BackButton
                    text=" < "
                    onPress={handleGoBackButton}
                />
                <Text style={styles.homeTitle}>
                    {service.name}
                </Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>
                    {service.description}
                </Text>
                <View style={styles.createStyle}>
                    <CustomButton
                        text="Create"
                        onPress={handleCreateButton}
                        type="PRIMARY"
                        bgColor={""}
                        Date time trigger fgColor={""}
                    />
                </View>
            </View>
            {/* <Text style={styles.homeTitle}>Popular 5-Minute Crafts workflows & automations</Text> */}
            {
                applets.map((applet) => (
                    <AppletAndServiceBox
                        key={applet.id}
                        title={applet.name}
                        description={applet.description}
                        author={applet.author}
                        user_nb={applet.frequency}
                        bgColor={applet.colour}
                        onPress={() => handleAppletButton(applet)}
                    />
                ))
            }
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
    },
    descriptionSericesAfterCreateButton: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    description: {
        fontSize: 20,
        margin: 30,
        color: 'white',
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    createStyle: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default ServicesDetails
