import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";
import ColorPicker from 'react-native-wheel-color-picker';
import Modal from 'react-native-modal';

import CustomerInput from "../../../components/CustomersInput";
import CustomerButton from "../../../components/CustomerButton";
import BackButton from "../../../components/BackButton/backButton";
import { queries } from "../../../../back-endConnection/querier";
import { getValue } from "../../../components/StoreData/storeData";

const Create = () => {
    const navigation = useNavigation();
    const route = useRoute();

    const { action, trigger } = route.params || {};

    const [appletName, setAppletName] = useState("");
    const [appletDescription, setAppletDescription] = useState("");
    const [appletTags, setAppletTags] = useState("");
    const [appletColor, setAppletColor] = useState("#000000");
    const [showColorPicker, setShowColorPicker] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const AppletsHome = () => {
        navigation.navigate("Applets");
    };

    const ChooseServices = () => {
        navigation.navigate("Choose services");
    };

    const InfoCreate = () => {
        console.log("Applet Name:", appletName);
        console.log("Applet Description:", appletDescription);
        console.log("Applet Tags:", appletTags);
        console.log("Applet Color:", appletColor);
    };

    const replaceOptWithSelect = (data) => {
        if (!data || typeof data !== 'object') return data;
        return JSON.parse(JSON.stringify(data).replace(/"opt"/g, '"select"'));
    };

    const handleCreate = async () => {
        if (!appletName || !appletDescription) {
            Alert.alert("Erreur", "Veuillez remplir tous les champs obligatoires !");
            return;
        }
        setIsLoading(true);

        try {
            const token = await getValue("token");
            const response = await queries.post(
                "/api/v1/my_applet",
                {
                    name: appletName,
                    description: appletDescription,
                    trigger: trigger,
                    consequences: action,
                    tags: appletTags,
                    colour: appletColor,
                },
                token
            );

            if (response.resp !== "success") {
                throw new Error("Erreur lors de l'envoi des données");
            }

            // const data = await response.json();
            console.log("Applet créé avec succès :", response);
            Alert.alert("Succès", "Applet créé avec succès !");

            setAppletName("");
            setAppletDescription("");
            setAppletTags("");
            setAppletColor("#000000");

            navigation.navigate("Applets");
        } catch (error) {
            console.error("Erreur:", error);
            Alert.alert("Erreur", "Échec de la création de l'applet.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled" >
            <Text style={styles.homeTitle}>Create</Text>
            <View style={styles.backButtonContainer}>
                <BackButton
                    text={"X"}
                    onPress={AppletsHome}
                />
            </View>
            <View style={styles.section}>
                <View style={styles.ifThisContainer}>
                    <CustomerButton
                        text="If"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                        <Text style={styles.addButtonText}>
                            {trigger.name || "Name of the trigger selected"}
                        </Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.ThenThatContainer}>
                    <CustomerButton
                        text="Then"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseServices}
                    >
                        <Text style={styles.addButtonText}>
                            {action.name || "Name of the action selected"}
                        </Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.DetailsApplets}>
                    <Text style={styles.label}>Your applet name</Text>
                    <CustomerInput
                        placeholder="Enter applet name"
                        value={appletName}
                        setValue={setAppletName}
                        secureTextEntry={false}
                    />

                    <Text style={styles.label}>Your applet description</Text>
                    <CustomerInput
                        placeholder="Enter applet description"
                        value={appletDescription}
                        setValue={setAppletDescription}
                        secureTextEntry={false}
                    />

                    <Text style={styles.label}>Your applet tags (Optional)</Text>
                    <CustomerInput
                        placeholder="Enter applet tags"
                        value={appletTags}
                        setValue={setAppletTags}
                        secureTextEntry={false}
                    />

                    <Text style={styles.label}>Your applet colour</Text>
                    <TouchableOpacity style={[styles.colorButton, { backgroundColor: appletColor }]} onPress={() => setShowColorPicker(true)}>
                        <Text style={styles.colorButtonText}>Pick a Color</Text>
                    </TouchableOpacity>

                    <Modal isVisible={showColorPicker} onBackdropPress={() => setShowColorPicker(false)}>
                        <View style={{ backgroundColor: "white", padding: 20, borderRadius: 10 }}>
                            <ColorPicker
                                color={appletColor}
                                onColorChangeComplete={(color) => {
                                    setAppletColor(color);
                                    console.log("Couleur en cours de sélection:", color);
                                }}
                                onColorSelected={color => {
                                    setAppletColor(color);
                                    console.log("Couleur sélectionnée:", color);
                                    setShowColorPicker(false);
                                }}
                                style={{ height: 200 }}
                            />
                        </View>
                    </Modal>
                </View>

                <View style={styles.ContinueContainer}>
                    <CustomerButton
                        text="Create"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        style={styles.ifThenText}
                        onPress={handleCreate}
                    />
                </View>
            </View>
        </ScrollView>
    );
};


const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 40,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 140,
        justifyContent: 'center',
        alignItems: 'center',
    },
    section: {
        alignItems: 'center',
    },
    ifThisContainer: {
        flexDirection: 'row',
        position: 'relative',
        justifyContent: 'center',
        alignItems: 'center',
        width: 300,
        height: 70,
        backgroundColor: 'black',
        borderRadius: 35,
        paddingHorizontal: 15,
        bottom: 130,
    },
    ThenThatContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
        width: 300,
        height: 70,
        backgroundColor: 'grey',
        borderRadius: 35,
        bottom: 80,
    },
    ContinueContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        width: 300,
        height: 70,
        backgroundColor: 'black',
        borderRadius: 35,
        bottom: 50,
    },
    ifThenText: {
        fontSize: 24,
        fontWeight: 'bold',
        marginRight: 10,
    },
    addButtonContainer: {
        width: 120,
        height: 50,
        borderRadius: 15,
        backgroundColor: 'white',
        justifyContent: 'center',
        alignItems: 'center',
        right: 30,
    },
    addButtonText: {
        color: 'black',
        fontSize: 14,
        fontWeight: 'bold',
    },
    backButtonContainer: {
        left: 160,
        marginTop: -60,
        marginBottom: 100,
    },
    DetailsApplets: {
        width: '100%',
        maxWidth: 400,
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
        bottom: 90,
    },
    label: {
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 10,
    },
    colorButton: {
        width: 150,
        height: 40,
        borderRadius: 10,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 10,
    },
    colorButtonText: {
        color: 'white',
        fontWeight: 'bold',
    },
    color: {
        marginBottom: 50,
    }
});

export default Create;
