import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import BackButton from "../../components/BackButton/backButton";

const Create = () => {
    const Navigation = useNavigation();

    const AppletsHome = () => {
        Navigation.navigate("Applets");
    }

    const ChooseServices = () => {
        Navigation.navigate("Choose services");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Text style={styles.homeTitle}>Create</Text>
            <BackButton
            text={"X"}
            onPress={AppletsHome}
            />
            <View style={styles.section}>
                <View style={styles.ifThisContainer}>
                    <CustomerButton
                    text="If This"
                    type="PRIMARY"
                    bgColor={"black"}
                    fgColor={""}
                    style={styles.ifThisButton}
                    />
                    <View style={styles.addButtonContainer}>
                        <CustomerButton
                            text="add"
                            type="PRIMARY"
                            bgColor={"white"}
                            fgColor={"black"}
                            onPress={ChooseServices}
                            style={styles.addButton}
                        />
                    </View>
                </View>
                <CustomerButton
                text="+"
                type="TERTIARY"
                bgColor={""}
                fgColor={"black"}
                />
                <CustomerButton
                text="Then That"
                type="PRIMARY"
                bgColor={"grey"}
                fgColor={""}
                />
            </View>
    </ScrollView>
    )
}

const styles = StyleSheet.create({
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 80,
        marginLeft: 150,
    },
    section: {
        alignItems: 'center',
        marginVertical: 20,
    },
    ifThisContainer: {
        flexDirection: 'row',
        position: 'relative',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
    },
    ifThisButton: {
        width: 250,
        height: 50,
    },
    addButtonContainer: {
        position: 'absolute',
        right: 10,
        width: 60,
        borderRadius: 80,
    },
    addButton: {
        paddingHorizontal: 10,
        paddingVertical: 5,
    }
})

export default Create