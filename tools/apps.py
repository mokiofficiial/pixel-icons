# drawable name -> (glyph, colour, [package/activity components])
# colour: "o" = orange, "g" = grey (alternating, like the reference sheet)
# Add your own apps here, then re-run generate.py.

APPS = {
    "phone": ("phone", "o", [
        "com.google.android.dialer/com.google.android.dialer.extensions.GoogleDialtactsActivity",
        "com.android.dialer/com.android.dialer.DialtactsActivity",
        "com.android.dialer/com.android.dialer.main.impl.MainActivity",
        "com.samsung.android.dialer/com.samsung.android.dialer.DialtactsActivity",
        "com.android.contacts/com.android.contacts.activities.TwelveKeyDialer",
        "com.android.contacts/com.android.contacts.DialtactsActivity",
    ]),
    "messages": ("message", "g", [
        "com.google.android.apps.messaging/com.google.android.apps.messaging.ui.ConversationListActivity",
        "com.samsung.android.messaging/com.android.mms.ui.ConversationComposer",
        "com.android.mms/com.android.mms.ui.MmsTabActivity",
        "com.android.mms/com.android.mms.ui.ConversationList",
    ]),
    "contacts": ("contacts", "o", [
        "com.google.android.contacts/com.android.contacts.activities.PeopleActivity",
        "com.android.contacts/com.android.contacts.activities.PeopleActivity",
        "com.samsung.android.app.contacts/com.samsung.android.contacts.contactslist.PeopleActivity",
    ]),
    "camera": ("camera", "g", [
        "com.google.android.GoogleCamera/com.android.camera.CameraLauncher",
        "com.android.camera/com.android.camera.Camera",
        "com.android.camera2/com.android.camera.CameraLauncher",
        "com.sec.android.app.camera/com.sec.android.app.camera.Camera",
        "com.oplus.camera/com.oplus.camera.Camera",
        "com.oneplus.camera/com.oneplus.camera.OPCameraActivity",
    ]),
    "gallery": ("gallery", "o", [
        "com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity",
        "com.miui.gallery/com.miui.gallery.activity.HomePageActivity",
        "com.sec.android.gallery3d/com.sec.android.gallery3d.app.GalleryActivity",
        "com.coloros.gallery3d/com.coloros.gallery3d.app.MainActivity",
        "com.android.gallery3d/com.android.gallery3d.app.GalleryActivity",
    ]),
    "settings": ("settings", "o", [
        "com.android.settings/com.android.settings.Settings",
        "com.android.settings/com.android.settings.MainSettings",
    ]),
    "clock": ("clock", "g", [
        "com.google.android.deskclock/com.android.deskclock.DeskClock",
        "com.android.deskclock/com.android.deskclock.DeskClock",
        "com.android.deskclock/com.android.deskclock.DeskClockTabActivity",
        "com.sec.android.app.clockpackage/com.sec.android.app.clockpackage.ClockPackage",
        "com.coloros.alarmclock/com.coloros.alarmclock.AlarmClock",
    ]),
    "calendar": ("calendar", "o", [
        "com.google.android.calendar/com.android.calendar.AllInOneActivity",
        "com.samsung.android.calendar/com.android.calendar.AllInOneActivity",
        "com.android.calendar/com.android.calendar.homepage.AllInOneActivity",
        "com.android.calendar/com.android.calendar.AllInOneActivity",
    ]),
    "calculator": ("calculator", "g", [
        "com.google.android.calculator/com.android.calculator2.Calculator",
        "com.miui.calculator/com.miui.calculator.cal.CalculatorActivity",
        "com.sec.android.app.popupcalculator/com.sec.android.app.popupcalculator.Calculator",
        "com.android.calculator2/com.android.calculator2.Calculator",
    ]),
    "files": ("folder", "o", [
        "com.google.android.apps.nbu.files/com.google.android.apps.nbu.files.home.HomeActivity",
        "com.google.android.documentsui/com.android.documentsui.LauncherActivity",
        "com.android.fileexplorer/com.android.fileexplorer.activity.FileActivity",
        "com.mi.android.globalFileexplorer/com.android.fileexplorer.FileExplorerTabActivity",
        "com.sec.android.app.myfiles/com.sec.android.app.myfiles.common.MainActivity",
    ]),
    "chrome": ("globe", "g", [
        "com.android.chrome/com.google.android.apps.chrome.Main",
        "com.brave.browser/com.google.android.apps.chrome.Main",
        "org.mozilla.firefox/org.mozilla.firefox.App",
        "com.sec.android.app.sbrowser/com.sec.android.app.sbrowser.SBrowserMainActivity",
        "com.microsoft.emmx/com.microsoft.ruby.Main",
    ]),
    "gmail": ("mail", "o", [
        "com.google.android.gm/com.google.android.gm.ConversationListActivityGmail",
        "com.microsoft.office.outlook/com.microsoft.office.outlook.MainActivity",
    ]),
    "maps": ("maps", "g", [
        "com.google.android.apps.maps/com.google.android.maps.MapsActivity",
    ]),
    "yt_music": ("music", "o", [
        "com.google.android.apps.youtube.music/com.google.android.apps.youtube.music.activities.MusicActivity",
        "com.miui.player/com.miui.player.ui.MusicBrowserActivity",
    ]),
    "play_store": ("play", "o", [
        "com.android.vending/com.android.vending.AssetBrowserActivity",
    ]),
    "youtube": ("youtube", "g", [
        "com.google.android.youtube/com.google.android.youtube.app.honeycomb.Shell$HomeActivity",
        "app.revanced.android.youtube/com.google.android.youtube.app.honeycomb.Shell$HomeActivity",
    ]),
    "whatsapp": ("chat_round", "o", [
        "com.whatsapp/com.whatsapp.Main",
        "com.whatsapp.w4b/com.whatsapp.Main",
    ]),
    "instagram": ("insta", "g", [
        "com.instagram.android/com.instagram.android.activity.MainTabActivity",
    ]),
    "telegram": ("plane", "o", [
        "org.telegram.messenger/org.telegram.ui.LaunchActivity",
        "org.telegram.messenger/org.telegram.messenger.DefaultIcon",
        "org.telegram.messenger.web/org.telegram.messenger.DefaultIcon",
    ]),
    "notes": ("notes", "g", [
        "com.google.android.keep/com.google.android.keep.activities.BrowseActivity",
        "com.samsung.android.app.notes/com.samsung.android.app.notes.memolist.MemoListActivity",
        "com.miui.notes/com.miui.notes.ui.NotesListActivity",
    ]),
    "weather": ("weather", "o", [
        "com.miui.weather2/com.miui.weather2.ActivityWeatherMain",
        "com.coloros.weather2/com.coloros.weather.main.view.WeatherMainActivity",
    ]),
    "downloads": ("download", "g", [
        "com.android.providers.downloads.ui/com.android.providers.downloads.ui.DownloadList",
    ]),
    "netflix": ("n", "o", [
        "com.netflix.mediaclient/com.netflix.mediaclient.ui.launch.UIWebViewActivity",
    ]),
    "prime_video": ("tv", "g", [
        "com.amazon.avod.thirdpartyclient/com.amazon.avod.thirdpartyclient.LauncherActivity",
        "com.jio.media.ondemand/com.jio.jioplay.tv.activities.HomeActivity",
    ]),
    "shopping": ("cart", "o", [
        "com.flipkart.android/com.flipkart.android.activity.HomeFragmentHolderActivity",
    ]),
    "wallet_card": ("card", "g", [
        "com.google.android.apps.walletnfcrel/com.google.commerce.tapandpay.android.cardlist.CardListActivity",
    ]),
    "x": ("x", "o", [
        "com.twitter.android/com.twitter.android.StartActivity",
    ]),
    "facebook": ("fb", "g", [
        "com.facebook.katana/com.facebook.katana.LoginActivity",
        "com.facebook.lite/com.facebook.lite.MainActivity",
    ]),
    "games": ("gamepad", "o", [
        "com.pubg.imobile/com.epicgames.ue4.SplashActivity",
        "com.dts.freefireth/com.dts.freefireth.FFMainActivity",
        "com.discord/com.discord.main.MainActivity",
    ]),
    "recorder": ("mic", "g", [
        "com.google.android.apps.recorder/com.google.android.apps.recorder.ui.main.MainActivity",
        "com.android.soundrecorder/com.android.soundrecorder.SoundRecorder",
        "com.sec.android.app.voicenote/com.sec.android.app.voicenote.main.VNMainActivity",
    ]),
    "linkedin": ("linkedin", "o", [
        "com.linkedin.android/com.linkedin.android.authenticator.LaunchActivity",
    ]),
    "snapchat": ("ghost", "g", [
        "com.snapchat.android/com.snapchat.android.LandingPageActivity",
    ]),
    "drive": ("drive", "o", [
        "com.google.android.apps.docs/com.google.android.apps.docs.app.NewMainProxyActivity",
    ]),
    "security": ("lock", "g", [
        "com.miui.securitycenter/com.miui.securityscan.MainActivity",
        "com.google.android.apps.authenticator2/com.google.android.apps.authenticator.AuthenticatorActivity",
    ]),
    "github": ("code", "o", [
        "com.github.android/com.github.android.main.MainActivity",
        "com.termux/com.termux.app.TermuxActivity",
    ]),
    "ai": ("sparkle", "g", [
        "com.openai.chatgpt/com.openai.chatgpt.MainActivity",
        "com.anthropic.claude/com.anthropic.claude.MainActivity",
        "com.google.android.apps.bard/com.google.android.apps.bard.shellapp.BardEntryPointActivity",
    ]),
    "spotify": ("waves", "o", [
        "com.spotify.music/com.spotify.music.MainActivity",
    ]),
    "meet": ("videocam", "g", [
        "com.google.android.apps.tachyon/com.google.android.apps.tachyon.MainActivity",
        "us.zoom.videomeetings/com.zipow.videobox.LauncherActivity",
    ]),
    "health": ("heart", "o", [
        "com.google.android.apps.fitness/com.google.android.apps.fitness.welcome.WelcomeActivity",
        "com.sec.android.app.shealth/com.sec.android.app.shealth.home.HomeActivity",
    ]),
    "news": ("news", "g", [
        "com.google.android.apps.magazines/com.google.apps.dots.android.app.activity.CurrentsStartActivity",
        "com.eterno/com.newshunt.appview.common.ui.activity.HomeActivity",
    ]),
    "books": ("book", "o", [
        "com.google.android.apps.books/com.google.android.apps.books.app.BooksActivity",
        "com.amazon.kindle/com.amazon.kindle.UpgradePage",
    ]),
    "rides": ("car", "g", [
        "com.ubercab/com.ubercab.presidio.app.core.root.RootActivity",
        "com.olacabs.customer/com.olacabs.customer.ui.SplashActivity",
        "com.rapido.passenger/com.rapido.passenger.SplashActivity",
    ]),
    "paytm": ("wallet", "o", [
        "net.one97.paytm/net.one97.paytm.landingpage.activity.AJRMainActivity",
        "net.one97.paytm/net.one97.paytm.AJRJarvisSplash",
    ]),
    "upi": ("upi", "g", [
        "com.google.android.apps.nbu.paisa.user/com.google.nbu.paisa.flutter.gpay.app.LauncherActivity",
        "com.phonepe.app/com.phonepe.app.ui.activity.Navigator_MainActivity",
        "com.phonepe.app/com.phonepe.app.launch.core.main.ui.MainActivity",
        "in.org.npci.upiapp/in.org.npci.upiapp.HomeActivity",
        "com.dreamplug.androidapp/com.dreamplug.androidapp.SplashActivity",
    ]),
    "hotstar": ("star_play", "o", [
        "in.startv.hotstar/in.startv.hotstar.WebViewActivity",
        "in.startv.hotstar/com.hotstar.MainActivity",
        "in.startv.hotstar/in.startv.hotstar.ui.splash.SplashActivity",
    ]),
    "amazon": ("bag", "g", [
        "in.amazon.mShop.android.shopping/com.amazon.mShop.splashscreen.StartupActivity",
        "com.amazon.mShop.android.shopping/com.amazon.mShop.splashscreen.StartupActivity",
        "com.myntra.android/com.myntra.android.SplashActivity",
        "com.meesho.supply/com.meesho.supply.main.SplashActivity",
    ]),
    "food": ("food", "o", [
        "com.application.zomato/com.application.zomato.activities.Splash",
        "in.swiggy.android/in.swiggy.android.activities.HomeActivity",
        "com.grofers.customerapp/com.grofers.customerapp.activities.ActivitySplash",
        "com.zeptoconsumerapp/com.zeptoconsumerapp.MainActivity",
    ]),
    "network": ("signal", "g", [
        "com.jio.myjio/com.jio.myjio.dashboard.activities.DashboardActivity",
        "com.myairtelapp/com.myairtelapp.activity.SplashActivity",
        "com.vodafone.selfservis/com.vodafone.selfservis.SplashActivity",
    ]),
}
