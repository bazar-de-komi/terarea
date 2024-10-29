import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

import CustomerButton from '../CustomerButton';

const BackButton = ({text, onPress}) => {
    return (
        <TouchableOpacity onPress={onPress}>
            <View style={styles.backStyle}>
                <CustomerButton
                text={text}
                onPress={onPress}
                type="TERTIARY"
                bgColor={""}
                fgColor={""}
                />
            </View>
        </TouchableOpacity>
    );
}
const styles = StyleSheet.create({
    backStyle: {
        marginBottom: 40,
        width: '180%',
        right: 150,
        // fontSize: 80,
        // alignSelf: 'center',
    },
});

export default BackButton;