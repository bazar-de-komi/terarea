import React from "react";
import { View, Image, StyleSheet, ScrollView} from 'react-native';

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png'
import ProfilLogo from '../../../assets/profilLogo.png';

const Header = () => {
    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.headerContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={ProfilLogo}
                    style={styles.profilLogo}
                />
            </View>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    headerContainer: {
        marginTop: 30,
        backgroundColor: '#e0d8d7',
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
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
})

export default Header