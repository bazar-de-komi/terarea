import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useRoute } from "@react-navigation/native";
import ColorPicker from 'react-native-wheel-color-picker';
import Modal from 'react-native-modal';

import CustomInput from "../../components/CustomInput/customInput";
import CustomButton from "../../components/CustomButton/customButton";
import Header from "../../components/Header/header";
import { queries } from "../../../back-endConnection/querier";
import { getValue, storeValue, deleteKey } from "../../components/StoreData/storeData";

const Create = () => {
    const navigation = useNavigation();
    const route = useRoute();

    const [storedTrigger, setStoredTrigger] = useState(null);
    const [storedAction, setStoredAction] = useState(null);
    const [appletName, setAppletName] = useState("");
    const [appletDescription, setAppletDescription] = useState("");
    const [appletTags, setAppletTags] = useState("");
    const [appletColor, setAppletColor] = useState("#000000");
    const [showColorPicker, setShowColorPicker] = useState(false);

    const { action, trigger } = route.params || {};

    const ChooseTriggersServices = () => {
        navigation.navigate("Choose options service for trigger");
    };

    const ChooseActionsServices = () => {
        navigation.navigate("Choose options service for action");
    };

    const handleCreate = async () => {
        if (!appletName || !appletDescription) {
            Alert.alert("Erreur", "Veuillez remplir tous les champs obligatoires !");
            return;
        }

        try {
            const token = await getValue("token");
            const response = await queries.post(
                "/api/v1/my_applet",
                {
                    name: appletName,
                    description: appletDescription,
                    trigger: storedTrigger,
                    consequences: storedAction,
                    tags: appletTags,
                    colour: appletColor,
                },
                token
            );

            if (response.resp !== "success") {
                throw new Error("Erreur lors de l'envoi des données");
            }
            Alert.alert("Succès", "Applet créé avec succès !");

            setAppletName("");
            setAppletDescription("");
            setAppletTags("");
            setAppletColor("#000000");
            deleteKey("trigger");
            deleteKey("action");

            navigation.navigate("Applets");
        } catch (error) {
            console.error("Erreur:", error);
            Alert.alert("Erreur", "Échec de la création de l'applet.");
        }
    };

    useEffect(() => {
        const storeTriggerAndAction = async () => {
            if (trigger !== undefined && trigger !== null) {
                await storeValue("trigger", JSON.stringify(trigger));
            }
            if (action !== undefined && action !== null) {
                await storeValue("action", JSON.stringify(action));
            }
        };
        storeTriggerAndAction();
    });

    useEffect(() => {
        const getTriggerAndAction = async () => {
            const getStoredTrigger = await getValue("trigger");
            const getStoredAction = await getValue("action");
            if (getStoredTrigger !== undefined && getStoredTrigger !== null) {
                setStoredTrigger(JSON.parse(getStoredTrigger));
            }
            if (getStoredAction !== undefined && getStoredAction !== null) {
                setStoredAction(JSON.parse(getStoredAction));
            }
        };
        getTriggerAndAction();
    });

    return (
        <ScrollView showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
            <Header />
            <Text style={styles.homeTitle}>Create</Text>
            <View style={styles.section}>
                <View style={styles.ifThisContainer}>
                    <CustomButton
                        text="If"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        onPress={null}
                        icon={null}
                    />
                    <TouchableOpacity
                        style={styles.addButtonContainer}
                        onPress={ChooseTriggersServices}
                    >
                        <Text style={styles.addButtonText}>
                            {storedTrigger?.name || "Add"}
                        </Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.ThenThatContainer}>
                    <CustomButton
                        text="Then"
                        type="PRIMARY"
                        bgColor={"transparent"}
                        fgColor={"white"}
                        onPress={null}
                        icon={null}
                    />
                    {storedTrigger && (
                        <TouchableOpacity
                            style={styles.addButtonContainer}
                            onPress={ChooseActionsServices}
                        >
                            <Text style={styles.addButtonText}>
                                {storedAction?.name || "Add"}
                            </Text>
                        </TouchableOpacity>
                    )}
                </View>

                {storedTrigger && storedAction && (
                    <View style={styles.DetailsApplets}>
                        <Text style={styles.label}>Your applet name</Text>
                        <CustomInput
                            placeholder="Enter applet name"
                            value={appletName}
                            setValue={setAppletName}
                            secureTextEntry={false}
                        />

                        <Text style={styles.label}>Your applet description</Text>
                        <CustomInput
                            placeholder="Enter applet description"
                            value={appletDescription}
                            setValue={setAppletDescription}
                            secureTextEntry={false}
                        />

                        <Text style={styles.label}>Your applet tags (Optional)</Text>
                        <CustomInput
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
                )}

                {appletName && appletDescription && appletColor && (
                    <View style={styles.ContinueContainer}>
                        <CustomButton
                            text="Create"
                            type="PRIMARY"
                            bgColor={"transparent"}
                            fgColor={"white"}
                            icon={null}
                            onPress={handleCreate}
                        />
                    </View>
                )}
            </View>
        </ScrollView>
    );
};


const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 40,
        fontWeight: 'bold',
        marginTop: 60,
        marginBottom: 180,
        textAlign: 'center',
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
