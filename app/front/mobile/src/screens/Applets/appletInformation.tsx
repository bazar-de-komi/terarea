import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TextInput, TouchableOpacity, Alert } from 'react-native'
import { Picker } from "@react-native-picker/picker";
import ColorPicker from 'react-native-wheel-color-picker';
import Modal from 'react-native-modal';
import { useRoute } from "@react-navigation/native";
import { useNavigation } from "@react-navigation/native";

import Header from "../../components/Header/header";
import { queries } from "../../../back-endConnection/querier";
import { getValue } from "../../components/StoreData/storeData";
import { parseJsonToForm, injectFormValuesIntoJson } from "../../Parsing/parseJson";

const AppletInformation = () => {
    const navigation = useNavigation();
    const route = useRoute();
    const { applet_id } = route.params || {};

    const [applet, setApplet] = useState({});
    const [loading, setLoading] = useState(true);

    const [appletName, setAppletName] = useState('');
    const [appletDescription, setAppletDescription] = useState('');
    const [appletColour, setAppletColour] = useState('#ffffff');
    const [appletTags, setAppletTags] = useState('');
    const [triggerFormFields, setTriggerFormFields] = useState<Record<string, any>[]>([]);
    const [reactionFormFields, setReactionFormFields] = useState<Record<string, any>[]>([]);
    const [showColorPicker, setShowColorPicker] = useState(false);

    const handleTriggerChange = (name: any, keyToChange: any, value: any) => {
        setTriggerFormFields((prev) =>
            prev.map((item) =>
                item.name === name ? { ...item, [keyToChange]: value } : item
            )
        );
    };

    const handleReactionChange = (name: any, keyToChange: any, value: any) => {
        setReactionFormFields((prev) =>
            prev.map((item) =>
                item.name === name ? { ...item, [keyToChange]: value } : item
            )
        );
    };

    const modifyApplet = async () => {
        try {
            const token = await getValue("token");
            const newTriggerJson = injectFormValuesIntoJson(applet.trigger, triggerFormFields);
            const newReactionJson = injectFormValuesIntoJson(applet.consequences, reactionFormFields);
            const response = await queries.put(
                `/api/v1/my_applet/${applet_id}`,
                {
                    name: appletName,
                    trigger: newTriggerJson,
                    consequences: newReactionJson,
                    tags: appletTags,
                    description: appletDescription,
                    colour: appletColour
                },
                token
            );
            if (response.resp === "success") {
                Alert.alert("Applet modified successfully !");
            }
        } catch (error) {
            Alert.alert("Error encountered while modifying applet !");
        }
    };

    const deleteApplet = async () => {
        try {
            const token = await getValue("token");
            const response = await queries.delete_query(`/api/v1/my_applet/${applet_id}`, {}, token);
            if (response.resp === "success") {
                Alert.alert("Applet deleted successfully !");
                navigation.goBack();
            }
        } catch (error) {
            Alert.alert("Error encountered while deleting applet !");
        }
    };

    const confirmDeleteApplet = () => {
        Alert.alert(
            "Confirm Deletion",
            "Are you sure you want to delete this applet? This action cannot be undone.",
            [
                { text: "Cancel", style: "cancel" },
                { text: "Delete", onPress: () => deleteApplet(), style: "destructive" }
            ]
        );
    };

    useEffect(() => {
        const fetchApplet = async () => {
            if (!applet_id) {
                console.error("Aucun applet_id fourni !");
                setLoading(false);
                return;
            }

            try {
                const token = await getValue("token");
                const response = await queries.get(`/api/v1/my_applet/${applet_id}`, {}, token);
                if (response.resp === "success") {
                    setApplet(response.msg);
                    setAppletName(response.msg.name);
                    setAppletDescription(response.msg.description);
                    setAppletTags(response.msg?.tags);
                    setAppletColour(response.msg.colour);
                    setTriggerFormFields(parseJsonToForm(response.msg.trigger));
                    setReactionFormFields(parseJsonToForm(response.msg.consequences));
                }
            } catch (error) {
                navigation.goBack();
            } finally {
                setLoading(false);
            }
        };

        fetchApplet();
    }, [applet_id]);

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            {loading ? (
                <ActivityIndicator size="large" color="#fff" />
            ) : (
                <View>
                    <View style={{ ...styles.mainContainer, backgroundColor: applet?.colour }}>
                        <Header />
                        <Text style={styles.appletTitle}>{applet.name}</Text>
                        <Text style={styles.appletDescription}>{applet.description}</Text>
                    </View>

                    <View style={styles.formContainer}>
                        <Text style={styles.sectionTitle}>Basic Applet Information</Text>

                        <Text style={styles.label}>Your applet name:</Text>
                        <TextInput style={styles.input} placeholder="Enter applet name" value={appletName} onChangeText={setAppletName} />

                        <Text style={styles.label}>Your applet description:</Text>
                        <TextInput style={styles.input} placeholder="Enter applet description" value={appletDescription} onChangeText={setAppletDescription} />

                        <Text style={styles.label}>Your applet tags (Optional):</Text>
                        <TextInput style={styles.input} placeholder="Enter tags" value={appletTags} onChangeText={setAppletTags} />

                        <Text style={styles.label}>Your applet colour:</Text>
                        <TouchableOpacity style={[styles.colorButton, { backgroundColor: appletColour }]} onPress={() => setShowColorPicker(true)}>
                            <Text style={styles.colorButtonText}>Pick a Color</Text>
                        </TouchableOpacity>

                        <Modal isVisible={showColorPicker} onBackdropPress={() => setShowColorPicker(false)}>
                            <View style={{ backgroundColor: "white", padding: 20, borderRadius: 10 }}>
                                <ColorPicker
                                    color={appletColour}
                                    onColorChangeComplete={(color) => {
                                        setAppletColour(color);
                                    }}
                                    onColorSelected={(color: any) => {
                                        setAppletColour(color);
                                        setShowColorPicker(false);
                                    }}
                                    style={{ height: 200 }}
                                />
                            </View>
                        </Modal>

                        <Text style={styles.sectionTitle}>Trigger: {applet.trigger.name}</Text>
                        {triggerFormFields.map((field, index) => (
                            <View key={index} style={styles.formGroup}>
                                <Text style={styles.label}>{field.name}</Text>
                                {field.type === 'input' && <TextInput style={styles.input} placeholder={field.placeholder} value={field.defaultValue} onChangeText={(itemValue) => handleTriggerChange(field.name, "defaultValue", itemValue)} />}
                                {field.type === 'textarea' && <TextInput style={styles.textArea} placeholder={field.placeholder} value={field.defaultValue} onChangeText={(itemValue) => handleTriggerChange(field.name, "defaultValue", itemValue)} multiline />}
                                {field.type === 'dropdown' && (
                                    <Picker
                                        selectedValue={field.defaultValue}
                                        onValueChange={(itemValue) => handleTriggerChange(field.name, "defaultValue", itemValue)}
                                    >
                                        {field.options.map((option, i) => (
                                            <Picker.Item key={i} label={option} value={option} />
                                        ))}
                                    </Picker>
                                )}
                            </View>
                        ))}

                        <Text style={styles.sectionTitle}>Reaction: {applet.consequences.name}</Text>
                        {reactionFormFields.map((field, index) => (
                            <View key={index} style={styles.formGroup}>
                                <Text style={styles.label}>{field.name}</Text>
                                {field.type === 'input' && <TextInput style={styles.input} placeholder={field.placeholder} value={field.defaultValue} onChangeText={(itemValue) => handleReactionChange(field.name, "defaultValue", itemValue)} />}
                                {field.type === 'textarea' && <TextInput style={styles.textArea} placeholder={field.placeholder} value={field.defaultValue} onChangeText={(itemValue) => handleReactionChange(field.name, "defaultValue", itemValue)} multiline />}
                                {field.type === 'dropdown' && (
                                    <Picker
                                        selectedValue={field.defaultValue}
                                        onValueChange={(itemValue) => handleReactionChange(field.name, "defaultValue", itemValue)}
                                    >
                                        {field.options.map((option, i) => (
                                            <Picker.Item key={i} label={option} value={option} />
                                        ))}
                                    </Picker>
                                )}
                            </View>
                        ))}

                        <View style={styles.buttonContainer}>
                            <TouchableOpacity style={styles.editButton} onPress={modifyApplet}>
                                <Text style={styles.buttonText}>✏️ Edit Applet</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.deleteButton} onPress={confirmDeleteApplet}>
                                <Text style={styles.buttonText}>🗑️ Delete Applet</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            )}
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    mainContainer: {
        marginTop: 30,
        borderRadius: 10,
        alignItems: 'center',
        padding: 5
    },
    appletTitle: {
        fontSize: 30,
        fontWeight: 'bold',
        color: 'black',
        textAlign: 'center',
        marginTop: 30
    },
    appletDescription: {
        fontSize: 18,
        marginTop: 10,
        marginBottom: 20,
        textAlign: 'center'
    },
    formContainer: {
        padding: 20
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginTop: 10,
        marginBottom: 20
    },
    label: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#333",
        marginBottom: 5,
    },
    input: {
        backgroundColor: "#fff",
        padding: 10,
        borderRadius: 5,
        borderWidth: 1,
        borderColor: "#ccc",
        marginBottom: 15,
    },
    textArea: {
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        borderRadius: 5,
        height: 80,
        marginBottom: 10
    },
    formGroup: {
        marginBottom: 15
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
    buttonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 20
    },
    editButton: {
        backgroundColor: "#4ea8de",
        padding: 15,
        borderRadius: 5,
    },
    deleteButton: {
        backgroundColor: "rgba(255, 38, 0, 0.767)",
        padding: 15,
        borderRadius: 5,
    },
    buttonText: {
        color: "white",
        fontWeight: "bold",
        textAlign: "center",
    }
})

export default AppletInformation;
