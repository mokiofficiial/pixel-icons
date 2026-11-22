package com.pixel.iconpack;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Installed apps that have no icon in the pack. Each app's ORIGINAL icon is
 * traced into a pixel icon on the phone (Tracer = same math as tools/trace.py).
 * COPY puts "Name | package/activity | g=<hex> c=o|g" lines on the clipboard:
 * paste them into tools/requests.txt, run tools/generate.py, rebuild.
 */
public class MissingActivity extends Activity {

    static final class Row {
        String name, comp;
        Tracer t;
        Bitmap original, tile;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final int dp = (int) getResources().getDisplayMetrics().density;
        PackageManager pm = getPackageManager();

        Set<String> themed = readAppfilter();
        Intent launcher = new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER);
        final List<Row> rows = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        for (ResolveInfo ri : pm.queryIntentActivities(launcher, 0)) {
            String comp = ri.activityInfo.packageName + "/" + ri.activityInfo.name;
            if (themed.contains(comp) || ri.activityInfo.packageName.equals(getPackageName())) continue;
            Row r = new Row();
            r.name = ri.loadLabel(pm).toString().replace("|", " ").trim();
            r.comp = comp;
            android.graphics.drawable.Drawable icon = ri.loadIcon(pm);
            r.original = Tracer.renderFull(icon);
            r.t = new Tracer(Tracer.render(icon));
            r.t.orange = Tracer.warm(r.original);
            r.tile = r.t.tile(192);
            rows.add(r);
        }
        rows.sort((a, b) -> a.name.compareToIgnoreCase(b.name));
        for (Row r : rows)
            sb.append(r.name).append(" | ").append(r.comp)
              .append(" | g=").append(r.t.hex()).append(" c=").append(r.t.orange ? "o" : "g").append('\n');
        final String text = sb.toString();
        for (String l : text.split("\n")) android.util.Log.i("PixelIcons", l);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.BLACK);
        root.setPadding(16 * dp, 40 * dp, 16 * dp, 16 * dp);

        TextView title = new TextView(this);
        title.setText("MISSING ICONS  " + rows.size()
                + "\nMade from each app's own icon. Copy -> tools/requests.txt -> generate.py");
        title.setTextColor(0xFF737373);
        title.setTypeface(Typeface.MONOSPACE);
        title.setTextSize(12);
        root.addView(title);

        TextView copy = new TextView(this);
        copy.setText("[ COPY LIST ]");
        copy.setTextColor(0xFFEE5A2D);
        copy.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        copy.setTextSize(16);
        copy.setPadding(0, 16 * dp, 0, 16 * dp);
        copy.setOnClickListener(v -> {
            ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("missing icons", text));
            Toast.makeText(this, rows.size() + " apps copied", Toast.LENGTH_SHORT).show();
        });
        root.addView(copy);

        GridView grid = new GridView(this);
        grid.setNumColumns(3);
        grid.setVerticalSpacing(16 * dp);
        grid.setAdapter(new BaseAdapter() {
            public int getCount() { return rows.size(); }
            public Object getItem(int i) { return rows.get(i); }
            public long getItemId(int i) { return i; }
            public View getView(int i, View convert, ViewGroup parent) {
                Row r = rows.get(i);
                LinearLayout cell = new LinearLayout(MissingActivity.this);
                cell.setOrientation(LinearLayout.VERTICAL);
                cell.setGravity(Gravity.CENTER_HORIZONTAL);
                LinearLayout pair = new LinearLayout(MissingActivity.this);
                pair.setGravity(Gravity.CENTER);
                ImageView orig = new ImageView(MissingActivity.this);
                orig.setImageBitmap(r.original);
                pair.addView(orig, new LinearLayout.LayoutParams(28 * dp, 28 * dp));
                ImageView made = new ImageView(MissingActivity.this);
                made.setImageBitmap(r.tile);
                pair.addView(made, new LinearLayout.LayoutParams(56 * dp, 56 * dp));
                cell.addView(pair);
                TextView name = new TextView(MissingActivity.this);
                name.setText(r.name.toUpperCase());
                name.setTextColor(0xFF737373);
                name.setTypeface(Typeface.MONOSPACE);
                name.setTextSize(10);
                name.setSingleLine(true);
                name.setGravity(Gravity.CENTER);
                cell.addView(name);
                return cell;
            }
        });
        root.addView(grid, new LinearLayout.LayoutParams(-1, 0, 1f));
        if (rows.isEmpty()) title.append("\n\nEvery app has an icon.");
        setContentView(root);
    }

    private Set<String> readAppfilter() {
        Set<String> out = new HashSet<>();
        Pattern p = Pattern.compile("ComponentInfo\\{([^}]+)\\}");
        try (BufferedReader r = new BufferedReader(new InputStreamReader(getAssets().open("appfilter.xml")))) {
            String line;
            while ((line = r.readLine()) != null) {
                Matcher m = p.matcher(line);
                if (m.find()) out.add(m.group(1));
            }
        } catch (Exception ignored) { }
        return out;
    }
}
