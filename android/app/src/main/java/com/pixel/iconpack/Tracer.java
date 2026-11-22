package com.pixel.iconpack;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.AdaptiveIconDrawable;
import android.graphics.drawable.Drawable;
import android.os.Build;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Original app icon -> 11 x 11 pixel outline, by math.
 * Java twin of tools/trace.py (same steps, same numbers) - read that file for the rules.
 */
final class Tracer {
    static final int S = 96, G = 11;

    final boolean[][] on = new boolean[G][G];
    boolean orange;

    /** Draw the icon at 96 x 96; adaptive icons use their foreground layer (centre 2/3). */
    static Bitmap render(Drawable d) {
        Bitmap bmp = Bitmap.createBitmap(S, S, Bitmap.Config.ARGB_8888);
        Canvas c = new Canvas(bmp);
        if (Build.VERSION.SDK_INT >= 26 && d instanceof AdaptiveIconDrawable
                && ((AdaptiveIconDrawable) d).getForeground() != null) {
            Drawable fg = ((AdaptiveIconDrawable) d).getForeground();
            int big = S * 3 / 2;                    // 108dp layer, 72dp visible
            fg.setBounds(-(big - S) / 2, -(big - S) / 2, S + (big - S) / 2, S + (big - S) / 2);
            fg.draw(c);
        } else {
            d.setBounds(0, 0, S, S);
            d.draw(c);
        }
        return bmp;
    }

    static int d2(int[] a, int[] b) {
        int r = a[0] - b[0], g = a[1] - b[1], bl = a[2] - b[2];
        return r * r + g * g + bl * bl;
    }

    Tracer(Bitmap bmp) {
        int[] px = new int[S * S];
        bmp.getPixels(px, 0, S, 0, 0, S, S);
        int[][] rgb = new int[S * S][];
        List<Integer> opaque = new ArrayList<>();
        for (int i = 0; i < S * S; i++) {
            rgb[i] = new int[]{Color.red(px[i]), Color.green(px[i]), Color.blue(px[i])};
            if (Color.alpha(px[i]) > 100) opaque.add(i);
        }
        if (opaque.isEmpty()) return;

        // k-means, fixed start = most common 4-bit colours
        Map<Integer, Integer> hist = new HashMap<>();
        for (int i : opaque) {
            int k = (rgb[i][0] >> 4) << 8 | (rgb[i][1] >> 4) << 4 | (rgb[i][2] >> 4);
            hist.merge(k, 1, Integer::sum);
        }
        List<Map.Entry<Integer, Integer>> order = new ArrayList<>(hist.entrySet());
        order.sort((a, b) -> !a.getValue().equals(b.getValue()) ? b.getValue() - a.getValue() : a.getKey() - b.getKey());
        List<int[]> cents = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : order) {
            int k = e.getKey();
            int[] c = {(k >> 8 & 15) * 16 + 8, (k >> 4 & 15) * 16 + 8, (k & 15) * 16 + 8};
            boolean far = true;
            for (int[] o : cents) if (d2(c, o) <= 3600) far = false;
            if (far) cents.add(c);
            if (cents.size() == 3) break;
        }
        int[] lab = new int[S * S];
        for (int it = 0; it < 6; it++) {
            long[][] sums = new long[cents.size()][4];
            for (int i : opaque) {
                int best = 0;
                for (int j = 1; j < cents.size(); j++) if (d2(rgb[i], cents.get(j)) < d2(rgb[i], cents.get(best))) best = j;
                lab[i] = best + 1;
                sums[best][0] += rgb[i][0]; sums[best][1] += rgb[i][1]; sums[best][2] += rgb[i][2]; sums[best][3]++;
            }
            for (int j = 0; j < cents.size(); j++)
                if (sums[j][3] > 0)
                    cents.set(j, new int[]{(int) (sums[j][0] / sums[j][3]), (int) (sums[j][1] / sums[j][3]), (int) (sums[j][2] / sums[j][3])});
        }

        // full-bleed background
        Map<Integer, Integer> bc = new HashMap<>();
        int nb = 0;
        for (int i = 0; i < S * S; i++) {
            int x = i % S, y = i / S;
            if (x == 0 || y == 0 || x == S - 1 || y == S - 1) { bc.merge(lab[i], 1, Integer::sum); nb++; }
        }
        int top = 0, topN = -1;
        for (Map.Entry<Integer, Integer> e : bc.entrySet()) if (e.getValue() > topN) { top = e.getKey(); topN = e.getValue(); }
        final int bg2 = (top != 0 && topN > 0.6 * nb) ? top : -1;

        int x0 = S, y0 = S, x1 = 0, y1 = 0, nfg = 0;
        Map<Integer, Integer> area = new HashMap<>();
        for (int i = 0; i < S * S; i++) {
            if (lab[i] == 0 || lab[i] == bg2) continue;
            int x = i % S, y = i / S;
            x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x + 1); y1 = Math.max(y1, y + 1);
            nfg++;
        }
        if (nfg == 0) return;
        double side = Math.max(x1 - x0, y1 - y0);
        double bx0 = (x0 + x1) / 2.0 - side / 2, by0 = (y0 + y1) / 2.0 - side / 2;

        for (int i : opaque) area.merge(lab[i], 1, Integer::sum);   // whole icon decides the colour

        int[][] grid = new int[G][G];
        for (int gy = 0; gy < G; gy++)
            for (int gx = 0; gx < G; gx++) {
                Map<Integer, Integer> votes = new HashMap<>();
                int tot = 0, nv = 0;
                for (int yy = (int) (by0 + gy * side / G); yy < (int) (by0 + (gy + 1) * side / G); yy++)
                    for (int xx = (int) (bx0 + gx * side / G); xx < (int) (bx0 + (gx + 1) * side / G); xx++) {
                        tot++;
                        if (xx >= 0 && xx < S && yy >= 0 && yy < S) {
                            int l = lab[yy * S + xx];
                            if (l != 0 && l != bg2) { votes.merge(l, 1, Integer::sum); nv++; }
                        }
                    }
                if (tot > 0 && nv >= 0.35 * tot) {
                    int best = 0, bn = -1;
                    for (Map.Entry<Integer, Integer> e : votes.entrySet())
                        if (e.getValue() > bn || (e.getValue() == bn && e.getKey() < best)) { best = e.getKey(); bn = e.getValue(); }
                    grid[gy][gx] = best;
                }
            }

        int n = outline(grid, true);
        if (n > 60) n = outline(grid, false);
        n = thin();
        if (n < 8) for (int y = 0; y < G; y++) for (int x = 0; x < G; x++) on[y][x] = grid[y][x] != 0;

        int big = 0, bigN = -1;
        for (Map.Entry<Integer, Integer> e : area.entrySet()) if (e.getValue() > bigN) { big = e.getKey(); bigN = e.getValue(); }
        int[] c = cents.get(big - 1);
        float[] hsl = new float[3];
        androidHsl(c, hsl);
        orange = hsl[2] > 0.35f && hsl[1] > 0.15f && hsl[1] < 0.85f && (hsl[0] < 0.17f || hsl[0] > 0.92f);
    }

    /** h, l, s in 0..1 (same order as Python colorsys.rgb_to_hls). */
    static void androidHsl(int[] c, float[] out) {
        float r = c[0] / 255f, g = c[1] / 255f, b = c[2] / 255f;
        float mx = Math.max(r, Math.max(g, b)), mn = Math.min(r, Math.min(g, b));
        float l = (mx + mn) / 2, s = 0, h = 0;
        if (mx != mn) {
            float d = mx - mn;
            s = l <= 0.5f ? d / (mx + mn) : d / (2 - mx - mn);
            if (mx == r) h = ((g - b) / d) / 6f;
            else if (mx == g) h = (2 + (b - r) / d) / 6f;
            else h = (4 + (r - g) / d) / 6f;
            if (h < 0) h += 1;
        }
        out[0] = h; out[1] = l; out[2] = s;
    }

    private int outline(int[][] grid, boolean colourEdges) {
        int n = 0;
        int[][] nb = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int y = 0; y < G; y++)
            for (int x = 0; x < G; x++) {
                on[y][x] = false;
                int l = grid[y][x];
                if (l == 0) continue;
                for (int[] d : nb) {
                    int nx = x + d[0], ny = y + d[1];
                    int m = (nx >= 0 && nx < G && ny >= 0 && ny < G) ? grid[ny][nx] : 0;
                    if (m == 0 || (colourEdges && m != l && m > l)) { on[y][x] = true; n++; break; }
                }
            }
        return n;
    }

    /** Zhang-Suen thinning, same as tools/trace.py thin(). */
    private int thin() {
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int step = 0; step < 2; step++) {
                List<int[]> kill = new ArrayList<>();
                for (int y = 0; y < G; y++) for (int x = 0; x < G; x++) {
                    if (!on[y][x]) continue;
                    boolean[] n = {at(x, y - 1), at(x + 1, y - 1), at(x + 1, y), at(x + 1, y + 1),
                                   at(x, y + 1), at(x - 1, y + 1), at(x - 1, y), at(x - 1, y - 1)};
                    int B = 0, A = 0;
                    for (int k = 0; k < 8; k++) { if (n[k]) B++; if (!n[k] && n[(k + 1) % 8]) A++; }
                    boolean p2 = n[0], p4 = n[2], p6 = n[4], p8 = n[6];
                    boolean ok = step == 0 ? !(p2 && p4 && p6) && !(p4 && p6 && p8)
                                           : !(p2 && p4 && p8) && !(p2 && p6 && p8);
                    if (B >= 2 && B <= 6 && A == 1 && ok) kill.add(new int[]{x, y});
                }
                for (int[] k : kill) on[k[1]][k[0]] = false;
                if (!kill.isEmpty()) changed = true;
            }
        }
        int c = 0;
        for (int y = 0; y < G; y++) for (int x = 0; x < G; x++) if (on[y][x]) c++;
        return c;
    }

    private boolean at(int x, int y) { return x >= 0 && x < G && y >= 0 && y < G && on[y][x]; }

    /** Colour rule on the WHOLE icon (adaptive: foreground + background layers). */
    static boolean warm(Bitmap full) {
        Bitmap one = full;
        int[] px = new int[S * S];
        one.getPixels(px, 0, S, 0, 0, S, S);
        Map<Integer, Integer> hist = new HashMap<>();
        for (int c : px) if (Color.alpha(c) > 100)
            hist.merge((Color.red(c) >> 4) << 8 | (Color.green(c) >> 4) << 4 | (Color.blue(c) >> 4), 1, Integer::sum);
        if (hist.isEmpty()) return false;
        int bestK = 0, bestN = -1;
        for (Map.Entry<Integer, Integer> e : hist.entrySet())
            if (e.getValue() > bestN || (e.getValue() == bestN && e.getKey() < bestK)) { bestK = e.getKey(); bestN = e.getValue(); }
        // average the colours near the most common one = the biggest colour region
        int[] c0 = {(bestK >> 8 & 15) * 16 + 8, (bestK >> 4 & 15) * 16 + 8, (bestK & 15) * 16 + 8};
        long r = 0, g = 0, b = 0, n = 0;
        for (int c : px) {
            if (Color.alpha(c) <= 100) continue;
            int[] v = {Color.red(c), Color.green(c), Color.blue(c)};
            if (d2(v, c0) < 3600) { r += v[0]; g += v[1]; b += v[2]; n++; }
        }
        float[] hsl = new float[3];
        androidHsl(new int[]{(int) (r / n), (int) (g / n), (int) (b / n)}, hsl);
        return hsl[2] > 0.35f && hsl[1] > 0.15f && hsl[1] < 0.85f && (hsl[0] < 0.17f || hsl[0] > 0.92f);
    }

    static Bitmap renderFull(Drawable d) {
        Bitmap bmp = Bitmap.createBitmap(S, S, Bitmap.Config.ARGB_8888);
        d.setBounds(0, 0, S, S);
        d.draw(new Canvas(bmp));
        return bmp;
    }

    String hex() {
        BigInteger v = BigInteger.ZERO;
        for (int y = 0; y < G; y++) for (int x = 0; x < G; x++) if (on[y][x]) v = v.setBit(y * G + x);
        String h = v.toString(16);
        while (h.length() < 31) h = "0" + h;
        return h;
    }

    /** Preview tile in the pack's style. */
    Bitmap tile(int size) {
        Bitmap b = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888);
        Canvas c = new Canvas(b);
        c.drawColor(Color.BLACK);
        int minX = G, minY = G, maxX = -1, maxY = -1;
        for (int y = 0; y < G; y++) for (int x = 0; x < G; x++) if (on[y][x]) {
            minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);
        }
        if (maxX < 0) return b;
        float u = size / 24f * 0.92f;            // 1 px of the 24 px grid
        float ox = (size - (maxX - minX + 1) * 2 * u) / 2, oy = (size - (maxY - minY + 1) * 2 * u) / 2;
        android.graphics.Paint p = new android.graphics.Paint();
        p.setColor(orange ? 0xFFEE5A2D : 0xFF5E5E5E);
        for (int y = minY; y <= maxY; y++) for (int x = minX; x <= maxX; x++) if (on[y][x])
            c.drawRect(ox + (x - minX) * 2 * u, oy + (y - minY) * 2 * u, ox + (x - minX + 1) * 2 * u, oy + (y - minY + 1) * 2 * u, p);
        return b;
    }
}
