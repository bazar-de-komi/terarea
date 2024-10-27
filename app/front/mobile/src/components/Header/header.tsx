import React, { useState } from "react";
import { View, Image, StyleSheet, ScrollView, TouchableOpacity, Modal, Text} from 'react-native';
import { useNavigation } from '@react-navigation/native';

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png'
import ProfilLogo from '../../../assets/profilLogo.png';

const Header = () => {
    const navigation = useNavigation();
    const [isSidebarVisible, setSidebarVisible] = useState(false);

    const openSidebar = () => setSidebarVisible(true);
    const closeSidebar = () => setSidebarVisible(false);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.headerContainer}>
                <TouchableOpacity onPress={() => navigation.navigate('Home')}>
                    <Image
                        source={AreaLogo}
                        style={styles.areaLogo}
                    />
                </TouchableOpacity>
                <TouchableOpacity onPress={openSidebar}>
                    <Image
                        source={ProfilLogo}
                        style={styles.profilLogo}
                    />
                </TouchableOpacity>

                <Modal
                    visible={isSidebarVisible}
                    transparent
                    animationType="slide"
                    onRequestClose={closeSidebar}
                >
                    <TouchableOpacity style={styles.modalOverlay} onPress={closeSidebar} />
                    <View style={styles.sidebar}>
                        <TouchableOpacity
                            onPress={() => {
                                navigation.navigate('Services');
                                closeSidebar();
                            }}
                            style={styles.menuItem}
                        >
                            <Text style={styles.menuText}>Profile</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            onPress={() => {
                                // Ajoute ici la logique pour "Log Out"
                                closeSidebar();
                            }}
                            style={styles.menuItem}
                        >
                            <Text style={styles.menuText}>Log Out</Text>
                        </TouchableOpacity>
                    </View>
                </Modal>
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
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    sidebar: {
        position: 'absolute',
        right: 0,
        top: 0,
        bottom: 0,
        width: 350,
        backgroundColor: 'white',
        padding: 20,
        justifyContent: 'center',
    },
    menuItem: {
        paddingVertical: 15,
    },
    menuText: {
        fontSize: 18,
    },
})

export default Header