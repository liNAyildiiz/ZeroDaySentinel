rule ZeroDaySentinel_Synthetic_Behavior_Marker
{
    meta:
        description = "Detects non-weaponized synthetic behavior markers used by ZeroDaySentinel."
        author = "Lina Yildiz"
        project = "ZeroDaySentinel"
        safe_for_demo = "true"

    strings:
        $marker_1 = "Synthetic suspicious behavior generated for defensive detection testing."
        $marker_2 = "ZeroDaySentinel"
        $marker_3 = "synthetic-telemetry-v0.2"

    condition:
        any of them
}
