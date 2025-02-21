import React from "react";
import { View, TextInput, StyleSheet } from 'react-native'

const CustomInput = ({ value, setValue, placeholder, secureTextEntry }) => {
    return (
        <View style={styles.customInputContainer}>
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
    customInputContainer: {
        backgroundColor: 'white',
        width: '70%',

        borderColor: '#e8e8e8',
        borderWidth: 1,
        borderRadius: 5,

        paddingHorizontal: 10,
        marginVertical: 5,
    },
})

export default CustomInput
