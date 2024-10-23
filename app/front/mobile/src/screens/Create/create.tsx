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

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Text style={styles.homeTitle}>Create</Text>
            <BackButton
            text={"X"}
            onPress={AppletsHome}
            />
            <View>
                <CustomerButton
                text="If This"
                type="PRIMARY"
                bgColor={"black"}
                fgColor={""}
                />
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
})

export default Create