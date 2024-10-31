import React, { useState, useEffect } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { WebView } from 'react-native-webview';
import { getValue } from '../../../components/StoreData/storeData';
import { queries } from '../../../../back-endConnection/querier';

const OAuthScreen = () => {
    const [authUrl, setAuthUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchAuthUrl = async () => {
            const url = await getValue("authUrl");
            setAuthUrl(url);
            setLoading(false); // Terminez le chargement une fois que l'URL est récupérée
        };

        fetchAuthUrl();
    }, []);

    const onNavigationStateChange = async (event: any) => {
        if (event.url.startsWith("https://pingpal.news/callback")) {
            const urlParams = new URLSearchParams(event.url.split('?')[1]);
            const code = urlParams.get('code');
            if (code) {
                let path: string = "/api/v1/oauth/callback?";
                path += event.url.split('?')[1];
                const response = await queries.post(path);
                console.log("Response:", response)
                // Fermez la WebView ou redirigez l'utilisateur selon vos besoins
                // navigation.goBack();
                // Envoyer le code au backend ou gérer l'authentification
            };
        }
    };

    if (loading) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    return (
        <View style={{ flex: 1 }}>
            {authUrl && (
                <WebView
                    source={{ uri: authUrl }}
                    onNavigationStateChange={onNavigationStateChange}
                    startInLoadingState
                    javaScriptEnabled={true}
                    domStorageEnabled={true}
                />
            )}
        </View>
    );
};

export default OAuthScreen;
