# dsv-server

1. Установить JRE-1.7 или JRE-1.8 на сервере.

2. Скопируйте dsv-server.jar и папку lib, keys на диск сервера. Сервер должен иметь доступ к тасикс.

3. Запуск.

	3.1. для запуска SOAP сервиса, наберите команду
            * На ОС Linux

                export TSA_URL=http://e-imzo.uz/cams/tst
                export TRUSTSTORE_FILE=keys/truststore.jks
                export TRUSTSTORE_PASSWORD=12345678

                java -Dfile.encoding=UTF-8 -jar dsv-server.jar -p 9090

            * На ОС Windows

                set TSA_URL=http://e-imzo.uz/cams/tst
                set TRUSTSTORE_FILE=keys/truststore.jks
                set TRUSTSTORE_PASSWORD=12345678

                java -Dfile.encoding=UTF-8 -jar dsv-server.jar -p 9090

	>приложение будет слушать сокет 127.0.0.1:9090, на экране (лог) напечатает URL SOAP по которому сторонние приложения могут обмениваться данными.
	>Пример:

            May 04, 2016 10:54:55 AM uz.yt.eimzo.dsv.server.Application run
            INFO: http://127.0.0.1:9090/dsvs/tsaproxy/v1
            May 04, 2016 10:54:55 AM uz.yt.eimzo.dsv.server.Application run
            INFO: http://127.0.0.1:9090/dsvs/cryptoauth/v1
            May 04, 2016 10:54:55 AM uz.yt.eimzo.dsv.server.Application run
            INFO: http://127.0.0.1:9090/dsvs/pkcs7/v1

	3.1. для справки наберите команду

		java -Dfile.encoding=UTF-8 -jar dsv-server.jar -h
	3.2. для вывода справки по API наберите команду

		java -Dfile.encoding=UTF-8 -jar dsv-server.jar -a
4. Для верификации подписи в документе PKCS#7 вызываете веб-метод verifyPkcs7 плагина Pkcs7.
        4.1. Пример json-ответа

            {
              "pkcs7Info": {
                "signers": [
                  {
                    "signerId": {
                      "issuer": "CN=ПЕТРОВ ПЕТР ПЕТРОВИЧ,T=Директор,O=YANGI TEXNOLOGIYALAR ILMIY-AXBOROT MARKAZI,OU=ЦРСОК ЭЦП,L=г.Ташкент ул.Абай 4,E=info@e-imzo.uz,C=UZ",
                      "subjectSerialNumber": "77777777"
                    },
                    "signingTime": "2016.11.08 07:03:17",
                    "signature": "92e1e9a9d48d9bbfb07e284106b6c192942145d471c7fb6c0abc3822e573fdc536d824867d7513f54a74d0f7bee8e3ba69ade761eb947599849c6f316cfc799b",
                    "digest": "922796f2dbefe6fd71056f527b5c6090aced4558eb84ea4bccd34bcef1756f26",
                    "certificate": [
                      {
                        "serialNumber": "77777777",
                        "subjectName": "CN=ИВАНОВ ИВАН ИВАНОВИЧ,Name=ИВАН,SURNAME=ИВАНОВ,O=PERFECT COMPANY,L=СЕРГЕЛИ т-н,ST=ТОШКЕНТ Ш.,C=UZ,UID=555555555,1.2.860.3.16.1.2=33333333333333,OU=Бошкарма,T=(noaniq),1.2.860.3.16.1.1=333333333,E=com@mail.ru,BusinessCategory=М.Ч.Ж  5-қисм",
                        "validFrom": "2016.09.29 11:07:41",
                        "validTo": "2018.09.29 11:07:40",
                        "issuerName": "CN=ПЕТРОВ ПЕТР ПЕТРОВИЧ,T=Директор,O=YANGI TEXNOLOGIYALAR ILMIY-AXBOROT MARKAZI,OU=ЦРСОК ЭЦП,L=г.Ташкент ул.Абай 4,E=info@e-imzo.uz,C=UZ",
                        "publicKey": {
                          "keyAlgName": "OZDST-1092-2009-2",
                          "publicKey": "MGAwGQYJKoZcAw8BAQIBMAwGCiqGXAMPAQECAQEDQwAEQMdEo+q34wBEhDjPFd79PrtfOBMBH7TaALUrL5j1jpjpUjCLpAL9Y155cO3/J7iscqyMa2cWP+nUYRHlgiPqhe0="
                        },
                        "signature": {
                          "signAlgName": "OZDST-1106-2009-2-AwithOZDST-1092-2009-2",
                          "signature": "98a8b6e74ce27ed83b7b0e387684187f7dfadff0f68520dad1da5b934703d21cb28d12b06f2aa7e49a103dc372decdcdde329bddd9b7e0d0eec78890de1b6666"
                        }
                      },
                      {
                        "serialNumber": "576a5ea5",
                        "subjectName": "CN=ПЕТРОВ ПЕТР ПЕТРОВИЧ,T=Директор,O=YANGI TEXNOLOGIYALAR ILMIY-AXBOROT MARKAZI,OU=ЦРСОК ЭЦП,L=г.Ташкент ул.Абай 4,E=info@e-imzo.uz,C=UZ",
                        "validFrom": "2016.06.22 14:54:15",
                        "validTo": "2021.06.22 14:54:15",
                        "issuerName": "E=info@mitc.uz,C=UZ,L=100047\\, Toshkent sh.\\, Amir Temur shoh ko’chasi\\, 4 uy,O=Axborot texnologiyalari va kommunikatsiyalarini riv-sh vazirligi,CN=ERI markazlarini ro'yxatdan o'tkazuvchi organi",
                        "publicKey": {
                          "keyAlgName": "OZDST-1092-2009-2",
                          "publicKey": "MGAwGQYJKoZcAw8BAQIBMAwGCiqGXAMPAQECAQEDQwAEQIEqwqeK0bkuOCZSnBcFhdtTkYk9ZtLR1mWZG4pN+g6SJsY0jFpbnDhq468dVSHjj971AuSXwbn1BdEhSaqM3gI="
                        },
                        "signature": {
                          "signAlgName": "OZDST-1106-2009-2-AwithOZDST-1092-2009-2",
                          "signature": "1a2047a8abd96ffaf2e23242a21d74c44d382cd45ed9dad5117d1e0c8e40b5cf0ff73092688fca635a9f8bb6fcd727b9c2916e9dcad00798768836129ccd535c"
                        }
                      }
                    ],
                    "OCSPResponse": "MIILo...j8to0",
                    "statusUpdatedAt": "2019.03.19 11:45:43",
                    "statusNextUpdateAt": "2019.03.19 11:46:43",
                    "verified": true,
                    "certificateVerified": true,
                    "trustedCertificate": {
                      "serialNumber": "575a613a",
                      "subjectName": "E=info@mitc.uz,C=UZ,L=100047\\, Toshkent sh.\\, Amir Temur shoh ko’chasi\\, 4 uy,O=Axborot texnologiyalari va kommunikatsiyalarini riv-sh vazirligi,CN=ERI markazlarini ro'yxatdan o'tkazuvchi organi",
                      "validFrom": "2016.06.10 11:49:30",
                      "validTo": "2036.06.10 11:49:30",
                      "issuerName": "E=info@mitc.uz,C=UZ,L=100047\\, Toshkent sh.\\, Amir Temur shoh ko’chasi\\, 4 uy,O=Axborot texnologiyalari va kommunikatsiyalarini riv-sh vazirligi,CN=ERI markazlarini ro'yxatdan o'tkazuvchi organi",
                      "publicKey": {
                        "keyAlgName": "OZDST-1092-2009-2",
                        "publicKey": "MGAwGQYJKoZcAw8BAQIBMAwGCiqGXAMPAQECAQEDQwAEQP6SA5IZiOsT/dsvORAxc+dPtw4UhuGLyRQ74Vf60luGQtUbvsFXqZuqsmCQLB2QtMKx8X8/L4awKeJ3lmYVT7I="
                      },
                      "signature": {
                        "signAlgName": "OZDST-1106-2009-2-AwithOZDST-1092-2009-2",
                        "signature": "5f5212c6e65993c963204b31ee43ac82e7ceb00f3ee8817f6aa1cb15e1b13b87462370cef7a201d0f6ad8b91b1ff46ee39bee1b2130791d03206fc97df6c864d"
                      }
                    },
                    "policyIdentifiers": [
                      "1.2.860.3.2.2.1.2.4",
                      "1.2.860.3.2.2.1.2.3",
                      "1.2.860.3.2.2.1.2.1",
                      "1.2.860.3.2.2.1.2.2"
                    ],
                    "certificateValidAtSigningTime": true,
                    "exception": "...."
                  }
                ],
                "documentBase64": "PD94....Q+DQo="
              },
              "success": true
            }
            * success - успешность операции
            * pkcs7Info.documentBase64 - подписанный документ в кодировке (Base64)
            * pkcs7Info.signers[N] - информация о том кто подписал документ.
            * pkcs7Info.signers[N].certificate[0] - информация о сертификате пользователя.
            * pkcs7Info.signers[N].certificate[1] - информация о сертификате ЦРК.
            * pkcs7Info.signers[N].certificate[2] - информация о корневом сертификате.
            * pkcs7Info.signers[N].OCSPResponse - OCSP ответ от сервера ЦРК
            * pkcs7Info.signers[N].signingTime - дата на компьютере пользователя при подписании
            * pkcs7Info.signers[N].verified - ЭЦП действительна
            * pkcs7Info.signers[N].certificateVerified - цепочка сертификатов действительна
            * pkcs7Info.signers[N].exception - ошибка при проверке подписи
            * pkcs7Info.signers[N].certificateValidAtSigningTime - сертификат действителен на дату подписи
            * UID  - Физ.ИНН
            * 1.2.860.3.16.1.2 - ПИНФЛ
            * 1.2.860.3.16.1.1 - Юр.ИНН
