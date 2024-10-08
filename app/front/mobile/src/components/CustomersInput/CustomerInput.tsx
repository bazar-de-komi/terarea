import React from "react";
import { View, Text, TextInput, StyleSheet } from 'react-native'

const CustomerInput = ({value, setValue, placeholder, secureTextEntry}) => {
    return (
        <View style={styles.CustomerInputContainer}>
            <TextInput
            value={value}
            onChangeText={setValue}
            placeholder={placeholder}
            secureTextEntry={secureTextEntry}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    CustomerInputContainer: {
        backgroundColor: 'white',
        width: '70%',

        borderColor: '#e8e8e8',
        borderWidth: 1,
        borderRadius: 5,

        paddingHorizontal: 10,
        marginVertical: 5,
    },
})

export default CustomerInput