Shader "WireframeShader"
{
    Properties
    {
        [HDR] _BaseColor ("Base Color", Color) = (0.2, 0.0, 0.4, 1.0)
        [HDR] _WireframeColor ("Wireframe Color", Color) = (0.8, 0.1, 0.0, 1.0)
        _WireframeThickness ("Wireframe Thickness", Range(0,5)) = 0.1 
        _WireframeSmoothing ("Wireframe Smoothing", Range(0,5)) = 0.1 
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        // wireframe resources: 
        // https://catlikecoding.com/unity/tutorials/advanced-rendering/flat-and-wireframe-shading/


        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float4 color : COLOR;
            };

            struct v2f
            {
                float4 color : COLOR;
                float4 vertex : SV_POSITION;
            };

            
            float4 _BaseColor, _WireframeColor;
            float _WireframeThickness, _WireframeSmoothing;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.color = v.color;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {

                float3 barys = i.color.rgb;
                float3 deltas = fwidth(barys);
                float3 thickness = deltas * _WireframeThickness;
                float3 smoothing = deltas * _WireframeSmoothing;
                barys = smoothstep(thickness, thickness + smoothing, barys);
                float minBary = min(barys.x, min(barys.y, barys.z));
                
                float4 finalColor = lerp(_WireframeColor, _BaseColor, minBary);

                return finalColor;
            }
            ENDCG
        }
    }
}
