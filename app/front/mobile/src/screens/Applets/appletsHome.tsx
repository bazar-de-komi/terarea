import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomInput from "../../components/CustomInput/customInput";
import Header from '../../components/Header/header';
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";

const Applets = () => {
    const navigation = useNavigation();
    const [applets, setApplets] = useState([]);
    const [search, setSearch] = useState("");

    const handleAppletButton = async (applet: any) => {
        navigation.navigate("Applet information", { applet_id: applet.id });
    };

    useEffect(() => {
        const getApplets = async () => {
            try {
                const token = await getValue("token");
                const getServicesResponse = await queries.get("/api/v1/my_applets", {}, token);
                setApplets(getServicesResponse.msg);
            } catch (error) {
                return;
            }
        };

        getApplets();

        const interval = setInterval(() => {
            getApplets();
        }, 500);

        return () => clearInterval(interval);
    });

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
            <Text style={styles.homeTitle}>My Applets</Text>
            <View style={styles.homeNavigation}>
            </View>
            <View style={styles.searchBar}>
                <CustomInput
                    value={search}
                    setValue={setSearch}
                    placeholder="Search applets"
                    secureTextEntry={false}
                />
            </View>
            {applets
                .filter(applet => {
                    if (!search.trim()) return true;

                    const searchWords = search.toLowerCase().split(/\s+/).filter(word => word.length > 0);

                    const matchesName = searchWords.some(word =>
                        applet.name?.toLowerCase().split(/\s+/).some((nameWord: any) => nameWord.includes(word))
                    );

                    const matchesDescription = searchWords.some(word =>
                        applet.description?.toLowerCase().split(/\s+/).some((descWord: any) => descWord.includes(word))
                    );

                    const matchesTags = searchWords.some(word =>
                        applet.tags?.toLowerCase().split(/\s+/).some((descWord: any) => descWord.includes(word))
                    );

                    return matchesName || matchesDescription || matchesTags;
                })
                .map((applet) => (
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
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        textAlign: 'center'
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    searchBar: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default Applets
