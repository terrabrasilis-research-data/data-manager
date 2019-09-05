declare module repositories {

    export interface User {
        name: string;
        image: string;
        id: number;
    }

    export interface CustomField {
    }

    export interface Service {
        name: string;
        id: number;
        host: string;
        ports: number[];
        created_on: Date;
    }

    export interface Repositorie {
        language: string;
        users: User[];
        name: string;
        id: number;
        keywords: string[];
        created_on: Date;
        maintainer: string;
        categories: string[];
        custom_fields: CustomField[];
        abstract: string;
        email: string;
        bbox: number[];
        services: Service[];
    }

}