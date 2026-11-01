plugins {
    alias(libs.plugins.android.application)
}

// Keep generated files out of the Google Drive workspace. Sync clients can lock
// incremental build directories while Gradle is trying to replace them.
layout.buildDirectory.set(
    file(System.getProperty("java.io.tmpdir")).resolve("ScoreKrijtApp-build/app")
)

android {
    namespace = "com.example.scorekrijtapp"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.example.scorekrijtapp"
        minSdk = 26
        targetSdk = 36
        versionCode = 288
        versionName = "2.8.8"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.activity)
    implementation(libs.androidx.constraintlayout)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}

// Google Drive zet in elke map een desktop.ini. Android Studio ziet die als resource en
// stopt met de fout "The file name must end with .xml or .png". Ruim ze voor de build op.
val removeDriveMetadata by tasks.registering(Delete::class) {
    delete(fileTree("src") { include("**/desktop.ini") })
}
tasks.matching { it.name.matches(Regex("(merge|package).*Resources")) }.configureEach {
    dependsOn(removeDriveMetadata)
}
