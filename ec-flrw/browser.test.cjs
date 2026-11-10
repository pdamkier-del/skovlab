/* Run with a local server on port 8000. Requires Playwright + Chromium. */
const { chromium } = require("playwright");
const assert = require("node:assert/strict");
(async () => {
  const browser = await chromium.launch({
    executablePath:
      process.env.CHROMIUM_PATH ||
      (require("node:fs").existsSync("/usr/bin/chromium")
        ? "/usr/bin/chromium"
        : chromium.executablePath()),
    headless: true,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage({
      viewport: { width: 1440, height: 1100 },
    }),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const plot = () =>
    page.locator("#plot").evaluate((el) => ({
      names: el.data.map((t) => t.name),
      layout: el.layout,
      lengths: el.data.map((t) => t.x.length),
      ys: el.data.map((t) => t.y),
    }));
  const settle = () => page.waitForTimeout(450);
  try {
    await page.goto("http://127.0.0.1:8000/ec-flrw/geometry-lab.html");
    await page.waitForSelector("#plot .scatterlayer .trace");
    let p = await plot();
    assert.equal(p.names.length, 2);
    assert.ok(p.names[0].startsWith("H "));
    assert.ok(p.names[1].startsWith("Ḣ "));
    assert.ok(p.layout.yaxis2);
    // Scrub and use a deliberately slow playback speed (must not stall at a sample).
    await page.locator("#speed").selectOption(".25");
    await page.locator("#play").click();
    await page.waitForTimeout(400);
    await page.locator("#play").click();
    assert.notEqual(await page.locator("#clock").innerText(), "τ -12");
    await page.locator("#time").fill("500");
    await page.locator("#time").dispatchEvent("input");
    assert.equal(await page.locator("#clock").innerText(), "τ 0");
    await page.locator("#progressive").check();
    await settle();
    p = await plot();
    assert.ok(p.ys[0].some((y) => y === null));
    await page.locator("#progressive").uncheck();
    await page.locator("#graph").selectOption("acceleration");
    await settle();
    p = await plot();
    assert.equal(p.names.length, 3);
    assert.equal(await page.locator("#clock").innerText(), "τ 0");
    await page.locator("#axes").selectOption("normalized");
    await settle();
    p = await plot();
    assert.ok(p.names.every((n) => n.includes("normalized")));
    assert.ok(p.ys.every((ys) => Math.max(...ys.map(Math.abs)) <= 1));
    await page.locator("#scale").selectOption("log");
    await settle();
    assert.match(await page.locator("#plotNote").innerText(), /omits/);
    await page.locator("#scale").selectOption("linear");
    await page.locator("#axes").selectOption("dual");
    await settle();
    // Toolbar zoom/pan state and reset; hover and legend use real pointer interaction.
    await page
      .locator("#plot")
      .evaluate((el) =>
        Plotly.relayout(el, { "xaxis.range": [-1, 1], dragmode: "pan" }),
      );
    assert.equal((await plot()).layout.dragmode, "pan");
    await page.locator("#view").click();
    await settle();
    assert.ok((await plot()).layout.xaxis.range[0] < -1);
    await page.locator("#plot .legend .traces").first().click();
    await settle();
    assert.equal(
      await page.locator("#plot").evaluate((el) => el.data[0].visible),
      "legendonly",
    );
    await page.locator("#plot .legend .traces").first().click();
    const box = await page.locator("#plot").boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + 150);
    await settle();
    assert.ok(await page.locator("#plot .hoverlayer").innerHTML());
    await page.locator("#events button").first().click();
    assert.match(
      await page.locator("#eventDetail").innerText(),
      /Positive finite scale factors: yes/,
    );
    await page.locator("#validate").click();
    assert.match(
      await page.locator("#convergence").innerText(),
      /Same endpoint/,
    );
    await page.locator("#compare").check();
    await settle();
    assert.equal((await plot()).names.length, 6);
    await page.locator("#compare").uncheck();
    await page.locator("#geometry").selectOption("ks");
    await settle();
    assert.equal(await page.locator("#flrwFields").isVisible(), false);
    assert.equal(await page.locator("#ksFields").isVisible(), true);
    assert.match(await page.locator("#events").innerText(), /Radial/);
    assert.match(await page.locator("#warnings").innerText(), /not proof/);
    // A volume plot must stay readable even when radial size grows by orders of magnitude.
    assert.equal(await page.locator("#graph").inputValue(), "collapse");
    p = await plot();
    assert.match(p.names[0], /Volume V/);
    assert.ok(p.ys[0].at(-1) < 0.00001);
    assert.ok(p.layout.yaxis.range[1] < 1.2);
    assert.equal(
      await page.locator("#plot").evaluate((el) => el.data[2].visible),
      "legendonly",
    );
    assert.equal(await page.locator("#axes").isDisabled(), true);
    await page.locator("#time").fill("950");
    await page.locator("#time").dispatchEvent("input");
    assert.match(
      await page.locator("#collapseStatus").innerText(),
      /Volume contracting/,
    );
    assert.match(
      await page.locator("#collapseStatus").innerText(),
      /Radial direction expanding; angular direction contracting/,
    );
    const selectedTime = await page.locator("#clock").innerText();
    await page.locator("#graph").selectOption("expansion");
    await page.locator("#scale").selectOption("signedlog");
    await settle();
    assert.equal(await page.locator("#axes").inputValue(), "dual");
    assert.equal(await page.locator("#clock").innerText(), selectedTime);
    const signedTraces = await page
      .locator("#plot")
      .evaluate((el) => el.data.map((t) => ({ y: t.y, raw: t.customdata })));
    for (const tr of signedTraces)
      for (let i = 0; i < tr.y.length; i++) {
        assert.ok(
          Math.abs(
            tr.y[i] -
              Math.sign(tr.raw[i]) * Math.log10(1 + Math.abs(tr.raw[i]) / 0.01),
          ) < 1e-10,
        );
      }
    assert.match(
      await page.locator("#plotNote").innerText(),
      /Tick labels and hover show original values/,
    );
    await page.locator("#collapseView").click();
    await settle();
    assert.equal(await page.locator("#clock").innerText(), selectedTime);
    await page.locator("#scale").selectOption("linear");
    await page.locator("#graph").selectOption("anisotropy");
    await settle();
    assert.equal((await plot()).names.length, 4);
    await page.locator("#T").fill("1");
    await settle();
    await page.locator("#validate").click();
    assert.match(
      await page.locator("#convergence").innerText(),
      /Same endpoint/,
    );
    await page.locator("#graph").selectOption("curvature");
    await settle();
    assert.equal((await plot()).names.length, 3);
    assert.ok((await plot()).layout.yaxis3);
    // Invalid input gives an explicit diagnostic, then recovers immediately.
    await page.locator("#Y0").fill("0");
    await settle();
    assert.match(
      await page.locator("#warnings").innerText(),
      /Invalid parameters/,
    );
    await page.locator("#Y0").fill("1");
    await settle();
    const downloadPromise = page.waitForEvent("download");
    await page.locator("#export").click();
    assert.match((await downloadPromise).suggestedFilename(), /ec-ks.csv/);
    // Geometry and graph switches retain parameters, reload retains saved settings.
    await page.locator("#geometry").selectOption("flrw");
    await settle();
    assert.equal(await page.locator("#T").inputValue(), "12");
    await page.locator("#geometry").selectOption("ks");
    await settle();
    assert.equal(await page.locator("#T").inputValue(), "1");
    await page.reload();
    await page.waitForSelector("#plot .scatterlayer .trace");
    assert.equal(await page.locator("#T").inputValue(), "1");
    for (const width of [390, 720, 1024]) {
      await page.setViewportSize({ width, height: 844 });
      await settle();
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth,
        ),
        false,
        `overflow at ${width}`,
      );
    }
    assert.deepEqual(errors, []);
    console.log(
      "Browser checks passed: playback, scrub, progressive trace, graphs, axes, hover, legend, zoom/pan/reset, events, convergence, comparison, parameters, export, persistence and responsive widths.",
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
