import React from "react";
import { View, Text, StyleSheet, Image, ScrollView, ImageBackground } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";

import MenuIcon from '../../../assets/menuIconWhite.png';
import AreaLogo from '../../../assets/authenticationLogo/AreaLogoWhite.png';
import Bg from '../../../assets/authenticationLogo/backgroundStart.jpg';

const Start = () => {
    const navigation = useNavigation();

    const handleStartButton = () => {
        navigation.navigate('Sign Up');
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <ImageBackground
                source={Bg}
                style={styles.headerContainer}
                imageStyle={{ borderRadius: 5 }}
            >
                <View style={styles.overlay} />
                
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={MenuIcon}
                    style={styles.profilLogo}
                />
                
                <Text style={styles.homeTitle}>Automation for business and home</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.title}>Save time and get more done</Text>
                <View style={styles.back}>
                    <CustomerButton
                        text="Start Today"
                        onPress={handleStartButton}
                        type="PRIMARY"
                        bgColor={"white"}
                        fgColor={"black"}
                    />
                </View>
            </ImageBackground>
            <Text style={styles.appletTitle}>Get started with any Applet</Text>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    headerContainer: {
        marginTop: 30,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
        height: 500,
        overflow: 'hidden',
    },
    overlay: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        borderRadius: 10,
    },
    areaLogo: {
        maxHeight: 50,
        marginTop: 20,
        marginLeft: -220,
    },
    profilLogo: {
        maxWidth: 30,
        maxHeight: 30,
        marginBottom: 60,
        marginTop: -40,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        color: 'white',
    },
    appletTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        color: 'black',
    },
    title: {
        fontSize: 28,
        margin: 30,
        color: 'white',
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default Start
