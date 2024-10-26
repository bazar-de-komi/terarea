import React from "react";
import { View, Image, StyleSheet, ScrollView, TouchableOpacity} from 'react-native';
import { useNavigation } from '@react-navigation/native';

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png'
import ProfilLogo from '../../../assets/profilLogo.png';

const Header = () => {
    const navigation = useNavigation();

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.headerContainer}>
                <TouchableOpacity onPress={() => navigation.navigate('Home')}>
                    <Image
                        source={AreaLogo}
                        style={styles.areaLogo}
                    />
                </TouchableOpacity>
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
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
    },
    areaLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: -180,
    },
    profilLogo: {
        maxHeight: 50,
        marginTop: -50,
        marginLeft: 300,
    },
})

export default Header