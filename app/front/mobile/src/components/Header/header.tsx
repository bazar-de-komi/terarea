import React, { useState } from "react";
import { View, Image, StyleSheet, ScrollView, TouchableOpacity, Modal, Text } from 'react-native';
import { useNavigation } from '@react-navigation/native';

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png'
import ProfilLogo from '../../../assets/profilLogo.png';
import { queries } from "../../../back-endConnection/querier";
import { deleteKey, getValue } from "../StoreData/storeData";

const Header = () => {
    const navigation = useNavigation();
    const [isSidebarVisible, setSidebarVisible] = useState(false);

    const openSidebar = () => setSidebarVisible(true);
    const closeSidebar = () => setSidebarVisible(false);

    const handleLogOut = async () => {
        await deleteKey("trigger");
        await deleteKey("action");
        try {
            const token = await getValue("token");
            await queries.post("/api/v1/logout", {}, token);
            await deleteKey("token");
            navigation.navigate('Sign In');
            closeSidebar();
        } catch (error) {
            await deleteKey("token");
            navigation.navigate('Sign In');
        }
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.headerContainer}>
                <TouchableOpacity onPress={async () => {
                    navigation.navigate('Applets');
                    await deleteKey("trigger");
                    await deleteKey("action");
                }}>
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
                    transparent={true}
                    animationType="none"
                    onRequestClose={closeSidebar}
                >
                    <TouchableOpacity
                        style={styles.modalOverlay}
                        onPress={closeSidebar}
                    />
                    <View style={styles.sidebar}>
                        <TouchableOpacity style={styles.menuItem}>
                            <Image
                                source={ProfilLogo}
                                style={styles.sideBarProfilLogo}
                            />
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.menuItem} onPress={closeSidebar}>
                            <Text style={styles.closeSideBarButton}>
                                X
                            </Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            onPress={async () => {
                                await deleteKey("trigger");
                                await deleteKey("action");
                                navigation.navigate('Create');
                                closeSidebar();
                            }}
                            style={styles.menuItem}
                        >
                            <Text style={styles.menuText}>Create</Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            onPress={async () => {
                                await deleteKey("trigger");
                                await deleteKey("action");
                                navigation.navigate('Profile');
                                closeSidebar();
                            }}
                            style={styles.menuItem}
                        >
                            <Text style={styles.menuText}>Profile</Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            onPress={async () => {
                                await deleteKey("trigger");
                                await deleteKey("action");
                                navigation.navigate('Applets');
                                closeSidebar();
                            }}
                            style={styles.menuItem}
                        >
                            <Text style={styles.menuText}>My applets</Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            onPress={() => {
                                handleLogOut();
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
    sideBarProfilLogo: {
        marginLeft: 230,
        marginTop: 30
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    closeSideBarButton: {
        marginTop: -65,
        fontSize: 20,
        fontWeight: 'bold',
    },
    sidebar: {
        position: 'absolute',
        right: 0,
        top: -400,
        bottom: 0,
        width: 350,
        backgroundColor: 'white',
        padding: 20,
        justifyContent: 'center',
    },
    menuItem: {
        paddingVertical: 15,
        marginLeft: 20,
        paddingBottom: 20
    },
    menuText: {
        fontSize: 18,
    },
})

export default Header
