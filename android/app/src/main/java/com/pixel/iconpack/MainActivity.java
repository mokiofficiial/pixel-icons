package com.pixel.iconpack;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

/** Shows every icon in the pack and lets you jump to Nova / Lawnchair to apply it. */
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final String[] names = getResources().getStringArray(R.array.icon_pack);
        final int dp = (int) getResources().getDisplayMetrics().density;

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.BLACK);
        root.setPadding(16 * dp, 40 * dp, 16 * dp, 16 * dp);

        TextView title = new TextView(this);
        title.setText("PIXEL ICONS  24PX\n" + names.length + " ICONS");
        title.setTextColor(0xFF8A8A8A);
        title.setTypeface(Typeface.MONOSPACE);
        title.setTextSize(14);
        title.setLetterSpacing(0.15f);
        root.addView(title);

        TextView apply = new TextView(this);
        apply.setText("[ APPLY ]");
        apply.setTextColor(0xFFFF5A26);
        apply.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        apply.setTextSize(16);
        apply.setPadding(0, 16 * dp, 0, 16 * dp);
        apply.setOnClickListener(v -> applyPack());

        TextView missing = new TextView(this);
        missing.setText("[ MISSING ICONS ]");
        missing.setTextColor(0xFF8A8A8A);
        missing.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        missing.setTextSize(16);
        missing.setPadding(24 * dp, 16 * dp, 0, 16 * dp);
        missing.setOnClickListener(v -> startActivity(new Intent(this, MissingActivity.class)));

        LinearLayout bar = new LinearLayout(this);
        bar.addView(apply);
        bar.addView(missing);
        root.addView(bar);

        GridView grid = new GridView(this);
        grid.setNumColumns(4);
        grid.setVerticalSpacing(12 * dp);
        grid.setHorizontalSpacing(12 * dp);
        grid.setAdapter(new BaseAdapter() {
            public int getCount() { return names.length; }
            public Object getItem(int i) { return names[i]; }
            public long getItemId(int i) { return i; }
            public View getView(int i, View convert, ViewGroup parent) {
                ImageView iv = convert instanceof ImageView ? (ImageView) convert : new ImageView(MainActivity.this);
                iv.setLayoutParams(new GridView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 72 * dp));
                iv.setScaleType(ImageView.ScaleType.FIT_CENTER);
                iv.setImageResource(getResources().getIdentifier(names[i], "drawable", getPackageName()));
                return iv;
            }
        });
        root.addView(grid, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));
        setContentView(root);
    }

    private void applyPack() {
        String pkg = getPackageName();
        Intent[] tries = {
            new Intent("com.teslacoilsw.launcher.APPLY_ICON_THEME")
                .setPackage("com.teslacoilsw.launcher")
                .putExtra("com.teslacoilsw.launcher.extra.ICON_THEME_TYPE", "GO")
                .putExtra("com.teslacoilsw.launcher.extra.ICON_THEME_PACKAGE", pkg),
            new Intent("app.lawnchair.APPLY_ICONS").putExtra("packageName", pkg),
            new Intent("ch.deletescape.lawnchair.APPLY_ICONS").putExtra("packageName", pkg),
            new Intent("ginlemon.smartlauncher.setGSLTHEME").putExtra("package", pkg),
        };
        for (Intent it : tries) {
            try {
                it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(it);
                return;
            } catch (ActivityNotFoundException ignored) { }
        }
        Toast.makeText(this, "Launcher settings > Icon pack > Pixel Icons", Toast.LENGTH_LONG).show();
    }
}
