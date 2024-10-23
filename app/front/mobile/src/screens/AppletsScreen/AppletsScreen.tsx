import React from "react";
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const AppletsScreen = () => {
    const Navigation = useNavigation();

    const signUp = () => {
        Navigation.navigate('Home');
    }

    const callApplets = () => {
        Navigation.navigate('Applets')
    }

    // const openDrawer = () => {
    //     Navigation.openDrawer();
    // }


    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                {/* <TouchableOpacity onPress={openDrawer}> */}
                    <Image
                        source={ProfilLogo}
                        style={styles.profilLogo}
                    />
                {/* </TouchableOpacity> */}
                <View style={styles.backStyle}>
                    <CustomerButton
                    text='<'
                    onPress={callApplets}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                    />
                </View>
                <Text style={styles.homeTitle}>5-Minute Crafts integrations</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>The 5-Minute Crafts Youtube channel is a</Text>
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
            <Text style={styles.homeTitle}>Get appletsScreensed with any Applet</Text>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    backContainer: {
        marginTop: 30,
        backgroundColor: "orange",
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
    },
    description: {
        fontSize: 20,
        margin: 30,
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
    backStyle: {
        marginBottom: 40,
        width: '180%',
        alignSelf: 'center',
        fontWeight: 'bold',
        fontSize: 35,
        color: "green",
    },
})

export default AppletsScreen